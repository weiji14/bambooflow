from packaging.version import Version

from bambooflow import __version__


def test_version():
    assert Version(version=__version__) >= Version(version="0.0.0")
