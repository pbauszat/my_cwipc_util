"""
View a point cloud using a Qt-based widget.

@todo: this script should be moved to the scripts folder.
"""
from PyQt5.QtCore import pyqtSlot, QTimer

from typing import Generator

from gui.base.pointcloud import Pointcloud
from gui.base.streamer import Streamer
from gui.openglwidget import OpenGLWidget
from gui.window import Window

"""
Application.
"""


class Application(Window):
    """
    Application class.
    """

    def __init__(self, fps: int = 30, point_count: int = 10000):
        """
        Constructor.
        """

        super().__init__()

        # Set the window title and status
        self.set_title("Pointcloud Viewer")
        self.set_status("Running.")

        # Create an OpenGL that will display the point cloud
        self._opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self._opengl_widget)

        # Create a streamer of synthetic pointclouds
        self._streamer: Streamer = Streamer(fps, point_count)
        self._generator: Generator[Pointcloud, None, None] = self._streamer.generator()

        # Set a timer to stream pointclouds at regular intervals
        tick_interval = int(1000.0 / float(fps))
        self._timer: QTimer = QTimer()
        self._timer.timeout.connect(self.tick)
        self._timer.start(tick_interval)

        # Show the window on start up
        self.show()

    @pyqtSlot()
    def tick(self):
        """
        Tick method.
        """

        pointcloud = next(self._generator)
        self._opengl_widget.set_pointcloud(pointcloud)


"""
Main.
"""


def main():
    # Create an application and run it
    application = Application()
    application.run()


if __name__ == '__main__':
    main()
