"""
View a point cloud using a Qt-based viewer.

@todo: this script should be moved to the scripts folder.
"""
from cwipc.gui.viewer import PointCloudViewer


def main():
    # Create the viewer and run it
    application = PointCloudViewer()
    application.show()
    application.run()


if __name__ == "__main__":
    main()
