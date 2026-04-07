"""
Wraps the CWIPC point cloud class.
"""
import numpy as np

# from ...util import cwipc_pointcloud_wrapper


class Pointcloud:
    """
    Pointcloud class.
    """

    def __repr__(self) -> str:
        """
        Humanly-readable representation.
        """

        return f"Pointcloud<{len(self.points)}>"

    def __str__(self) -> str:
        """
        Humanly-readable representation.
        """

        return f"Pointcloud<{len(self.points)}>"

    @property
    def points(self) -> np.ndarray:
        """
        Returns the points as compact numpy array.

        The format is 
        """

        data = [[0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0]]

        return np.array(data, dtype=np.float32)
