"""
A controller class that holds a virtual camera and processes user input.
"""
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent

from .base.transform import Transform


class Controller:
    """
    Controller class.
    """

    def __init__(self, move_speed: float = 0.1, mouse_speed: float = 1.0, wheel_speed: float = 1.0) -> None:
        """
        Constructor.

        :param move_speed: The move speed.
        :param mouse_speed: The mouse speed.
        :param wheel_speed: The wheel speed.
        """

        self._transform: Transform = Transform()
        self._move_speed: float = move_speed
        self._mouse_speed: float = mouse_speed
        self._wheel_speed: float = wheel_speed
        self._mouse_click_position: QPoint = QPoint()

    @property
    def transform(self) -> Transform:
        """
        Returns the current transform.

        :return: The current transform.
        """

        return self._transform

    def key_press(self, event: QKeyEvent) -> None:
        """
        Handles key presses.

        :param event: The key event.
        :return: None.
        """

        if event.key() == Qt.Key_A:
            self._transform.translate(self._move_speed, 0.0, 0.0)
            event.accept()
        if event.key() == Qt.Key_D:
            self._transform.translate(-self._move_speed, 0.0, 0.0)
            event.accept()

    def mouse_press(self, event: QMouseEvent) -> None:
        """
        Handles mouse presses.

        :param event: The key event.
        :return: None.
        """

        self._mouse_click_position = event.localPos()

    def mouse_move(self, event: QMouseEvent) -> None:
        """
        Handles mouse movements.

        :param event: The key event.
        :return: None.
        """

        if event.buttons() == Qt.LeftButton:
            difference = self._mouse_click_position - event.localPos()
            self._transform.rotate(difference.x() * self._mouse_speed, 0.0, 1.0, 0.0)
            self._mouse_click_position = event.localPos()
            event.accept()

    def wheel(self, event: QWheelEvent) -> None:
        """
        Handles mouse wheel events.

        :param event: The key event.
        :return: None.
        """

        pass
