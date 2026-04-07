"""
Provides the base class for window-based Qt applications.
"""
import pathlib
import PyQt5.uic

from .qtbase import QtBase


class Window(QtBase):
    """
    Window class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """

        super().__init__()
        # Load base UI from file
        ui_file = pathlib.Path(__file__).with_name("window.ui")
        PyQt5.uic.loadUi(ui_file, self)

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
