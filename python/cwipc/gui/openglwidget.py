"""
A Qt OpenGLWidget that allows display and exploration of a pointcloud.
"""
import numpy as np
import OpenGL.GL.shaders as gl_shaders

from OpenGL.GL import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLShader, QOpenGLShaderProgram, QSurfaceFormat, QOpenGLVertexArrayObject
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QOpenGLWidget, QWidget
from typing import Optional

from .base.pointcloud import Pointcloud
from .base.transform import Transform
from .controller import Controller
from .shaders import VERTEX_SHADER, FRAGMENT_SHADER


class OpenGLWidget(QOpenGLWidget):
    """
    OpenGLWidget class.
    """

    def __init__(self, parent: QWidget) -> None:
        """
        Constructor.

        :param parent: The parent widget.
        """

        super().__init__(parent)

        # Setup strong focus and mouse tracking for user-control
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        # Setup surface format
        surface_format = QSurfaceFormat.defaultFormat()
        surface_format.setVersion(4, 3)
        surface_format.setProfile(QSurfaceFormat.CoreProfile)
        surface_format.setOption(QSurfaceFormat.DebugContext)   # Toggle debugging off for more performance
        surface_format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        surface_format.setRedBufferSize(8)
        surface_format.setGreenBufferSize(8)
        surface_format.setBlueBufferSize(8)
        surface_format.setAlphaBufferSize(8)
        surface_format.setDepthBufferSize(24)
        surface_format.setStencilBufferSize(0)
        surface_format.setSamples(16)
        surface_format.setSwapInterval(0)
        self.setFormat(surface_format)

        # Define internal shaders and buffers (they must be initialized later in the initializeGL() method)
        self._shader_program: QOpenGLShaderProgram = QOpenGLShaderProgram()
        self._vertex_array: QOpenGLVertexArrayObject = QOpenGLVertexArrayObject()
        self._vertex_buffer: QOpenGLBuffer = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._pointcloud: Optional[Pointcloud] = None

        # A controller to handle user-input
        self._controller: Controller = Controller()

    """
    Rendering.
    """

    def initializeGL(self) -> None:
        """
        Initialize the OpenGL widget.

        This method performs the delayed initialization and is only called when there is an active OpenGL context.

        :return: None.
        """

        super().initializeGL()

        # Build shader program
        self._shader_program.addShaderFromSourceCode(QOpenGLShader.Vertex, VERTEX_SHADER)
        self._shader_program.addShaderFromSourceCode(QOpenGLShader.Fragment, FRAGMENT_SHADER)
        if not self._shader_program.link():
            raise RuntimeError(f"OpenGLWidget shader linking failed ('{self._shader_program.log()}').")

        # Delayed creation of vertex array and vertex buffer
        self._vertex_array.create()
        self._vertex_buffer.create()
        self._vertex_buffer.setUsagePattern(QOpenGLBuffer.DynamicDraw)

        # Setup OpenGL default globals
        glClearColor(0.2, 0.2, 0.2, 1.0)

    def paintGL(self) -> None:
        """
        Paint the OpenGL widget.

        :return: None.
        """

        super().paintGL()

        # If a new pointcloud has been set, upload it here where an OpenGL context is safely guaranteed
        if self._pointcloud:
            vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]
            vertices = np.array(vertices, dtype=np.float32).flatten()
            self._vertex_buffer.bind()
            self._vertex_buffer.allocate(vertices.data, vertices.nbytes)

            self._vertex_array.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)

            self._vertex_array.release()
            self._vertex_buffer.release()
            self._pointcloud = None

        # Perform the actual rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self._shader_program.bind()
        self._shader_program.setUniformValue("transform", self._controller.transform)
        self._vertex_array.bind()
        glDrawArrays(GL_TRIANGLES, 0, 3)

        self._vertex_array.release()
        self._shader_program.release()

    def set_pointcloud(self, pointcloud: Pointcloud) -> None:
        """
        Sets the current pointcloud.

        :param pointcloud: A pointcloud instance.
        :return: None.
        """

        self._pointcloud = pointcloud
        self.update()

    """
    User Control.
    """

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key-press events.

        :param event: The event.
        :return: None.
        """

        self._controller.key_press(event)
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse-press events.

        :param event: The event.
        :return: None.
        """

        self._controller.mouse_press(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handles mouse-move events.

        :param event: The event.
        :return: None.
        """

        self._controller.mouse_move(event)
        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Handles mouse-wheel events.

        :param event: The event.
        :return: None.
        """

        self._controller.wheel(event)
        super().wheelEvent(event)
