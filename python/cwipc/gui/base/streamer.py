"""
A utility class that streams pointclouds.
"""
from typing import Generator

from cwipc.util import cwipc_activesource_wrapper, cwipc_synthetic

from .pointcloud import Pointcloud


class Streamer:
    """
    Pointcloud streamer.
    """

    def __init__(self, fps: int, point_count: int) -> None:
        """
        Init.

        :param fps: The frame rate.
        :param point_count: Number of points.
        """

        # Create a synthetic generator and start it
        generator = cwipc_synthetic(fps, point_count)
        started = generator.start()
        if not started:
            raise RuntimeError("Grabber not started")
        if not generator.available(True):
            raise RuntimeError("Grabber must be available")

        # Store internals
        self._generator: cwipc_activesource_wrapper = generator

    def generator(self) -> Generator[Pointcloud, None, None]:
        """
        Yields a stream of point clouds.
        """

        while True:
            # todo: this is currently throwing an exception!
            # pointcloud = self._generator.get()
            #if not pointcloud:
            #    raise RuntimeError("Must have a point cloud")

            #assert isinstance(pointcloud, Pointcloud), "Wrong pointcloud instance"
            #yield pointcloud

            yield Pointcloud()
