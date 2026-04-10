"""
A qt-based point cloud viewer.
"""
import pathlib
import queue
import time
import threading

from PyQt5.QtCore import QTimer, pyqtSlot
from typing import Generator

from .utility.pointcloud import PointCloud
from .streamer import Streamer
from .widget.pointcloudwidget import PointCloudWidget
from .window import MainWindow


class PointCloudViewer(MainWindow):
    """
    PointCloudViewer class.
    """

    def __init__(self, fps: int = 30) -> None:
        """
        Constructor.

        :param fps: The number of frames per second (update rate).
        """

        super().__init__()

        # (1) Load the UI from file
        ui_file = pathlib.Path(__file__).with_name("viewer.ui")
        self.load_ui(ui_file)
        self.set_title("PointCloud Viewer")
        self.set_status("Running.")

        # (2) Create a point cloud viewer widget and make it the central widget
        self._point_cloud_widget: PointCloudWidget = PointCloudWidget(self)
        self.setCentralWidget(self._point_cloud_widget)

        # (3) Create a point cloud streamer
        self._streamer: Streamer = Streamer(fps, 10000)
        self._generator: Generator[PointCloud, None, None] = self._streamer.generator()

        # (4) Create a producer-consumer queue and producer thread
        self._queue: queue.Queue = queue.Queue(maxsize=1)
        self._producer_thread: threading.Thread = threading.Thread(target=self._produce, daemon=True)

        # (5) Consumer will be the main thread and a tick function is used to pull from the queue at regular intervals
        self._timer: QTimer = QTimer()
        self._last_time: int = time.perf_counter_ns()

        # (6) Start the producer thread and the Qt timer
        self._producer_thread.start()
        self._timer.timeout.connect(self._tick)
        self._timer.start(int(1000.0 / float(fps)))

    def set_title(self, title: str) -> None:
        """
        Set window title.

        :param title: The new window title.
        :return: None.
        """

        self.setWindowTitle(title)

    def set_status(self, message: str) -> None:
        """
        Set status text.

        :param message: The new status message.
        :return: None.
        """

        self.statusbar.showMessage(message)

    """
    Internals.
    """

    def _produce(self) -> None:
        """
        Load point clouds in a separate thread and put them in the producer-consumer queue.

        :return: None.
        """

        while True:
            try:
                # Get a new point cloud
                point_cloud = next(self._generator)
            except StopIteration:
                # Otherwise, break the production loop
                break

            # Put the point cloud in the queue
            self._queue.put(point_cloud)

        # Put None in the queue to signal the end of production
        self._queue.put(None)

    @pyqtSlot()
    def _tick(self) -> None:
        """
        Updates the point cloud at a fixed frame rate.

        :return: None.
        """

        # Save current time
        current_time = time.perf_counter_ns()

        # Get a new point cloud from the queue (or wait until one is in it)
        point_cloud = self._queue.get()

        if point_cloud:
            # Update the point cloud widget
            self._point_cloud_widget.set_point_cloud(point_cloud)
        else:
            # Production stopped
            self._timer.stop()

        # Processed the point cloud, queue is free now
        self._queue.task_done()

        # Update timing info
        elapsed_time_ms = (current_time - self._last_time) / (10 ** 6)
        self.set_title(f"PointCloud Viewer ({elapsed_time_ms} ms)")
        self._last_time = current_time
