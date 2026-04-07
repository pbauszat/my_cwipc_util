"""
A basic transformation class.
"""
import enum

from PyQt5.QtGui import QMatrix4x4


class Transform(QMatrix4x4):
    """
    Transform class.
    """

    class Unit(enum.Enum):
        RADIANS = enum.auto()
        DEGREES = enum.auto()

    def __init__(self) -> None:
        """
        Constructor.
        """

        super().__init__()
