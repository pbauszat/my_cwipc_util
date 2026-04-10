"""
The Renderer class.
"""
import OpenGL.GL.shaders as gl_shaders

from ctypes import c_void_p
from OpenGL.GL import *

from .shaders import VERTEX_SHADER_SIMPLE, FRAGMENT_SHADER_SIMPLE

from ..utility.pointcloud import PointCloud
from ..utility.transform import Transform


class Renderer:
    """
    The Renderer class.
    """

    def __init__(self):
        """
        Constructor.
        """

        self._point_count: int = 0
        self._transform: Transform = Transform()
        self._vertex_buffer: GLuint = 0
        self._vertex_array: GLuint = 0
        self._shader_program: GLuint = 0

    def initialize(self) -> None:
        """
        Initialize the rendering.

        :return: None.
        """

        # Initialize internal buffers and arrays
        self._vertex_buffer = glGenBuffers(1)
        self._vertex_array = glGenVertexArrays(1)
        self._shader_program = gl_shaders.compileProgram(
            gl_shaders.compileShader(VERTEX_SHADER_SIMPLE, GL_VERTEX_SHADER),
            gl_shaders.compileShader(FRAGMENT_SHADER_SIMPLE, GL_FRAGMENT_SHADER),
        )

        # Define constant OpenGL settings
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_DEPTH_TEST)

    def resize(self, width: int, height: int) -> None:
        """
        Handle viewpoint resizes.

        :return: None.
        """

        pass

    def render(self):
        """
        Render the content.

        :return: None.
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self._shader_program)
        location = glGetUniformLocation(self._shader_program, "transform")
        glUniformMatrix4fv(location, 1, GL_TRUE, self._transform.data)

        glBindVertexArray(self._vertex_array)
        glDrawArrays(GL_POINTS, 0, self._point_count)

        glBindVertexArray(0)
        glUseProgram(0)

    def update_data(self, point_cloud: PointCloud) -> None:
        """
        Updates the point cloud data.

        :param point_cloud: The point cloud.
        :return: None.
        """

        self._point_count = point_cloud.count

        # Update point cloud data in the vertex buffer
        if point_cloud.count > 0:
            glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
            glBufferData(GL_ARRAY_BUFFER, point_cloud.points, GL_STATIC_DRAW)

            vertex_shift = 6 * 4
            glBindVertexArray(self._vertex_array)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex_shift, None)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertex_shift, c_void_p(12))
            glEnableVertexAttribArray(1)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def update_transform(self, transform: Transform) -> None:
        """
        Updates the transformation.

        :param transform: The transformation.
        :return: None.
        """

        self._transform = transform
