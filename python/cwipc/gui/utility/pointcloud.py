"""
A point cloud wrapper class.
"""
from typing import Optional

from ...util import cwipc_pointcloud_wrapper


class PointCloud:
    """
    PointCloud class.
    """

    def __init__(self, source: Optional[cwipc_pointcloud_wrapper] = None) -> None:
        """
        Constructor.

        :param source: The point cloud source.
        """

        self._source: Optional[cwipc_pointcloud_wrapper] = source

    def __repr__(self) -> str:
        """
        Returns a string representation of the instance.

        :return: A string representation of the instance.
        """

        return f"PointCloud<{self.count}>"

    def __str__(self) -> str:
        """
        Returns a humanly-readable string representation of the instance.

        :return: A humanly-readable string representation of the instance.
        """

        return f"PointCloud<{self.count} points>"

    @property
    def count(self) -> int:
        """
        Returns the number of points in the point cloud.

        :return: The number of points.
        """

        return self._source.count() if self._source else 0
