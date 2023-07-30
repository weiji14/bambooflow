"""
Tests for aiter datapipes.
"""
import pytest

from bambooflow.datapipes import AsyncIterDataPipe


# %%
@pytest.fixture(scope="function", name="datapipe")
def fixture_datapipe():
    """
    An instance of an AsyncIterDataPipe to use in the tests.
    """

    class AIDP(AsyncIterDataPipe):
        def __aiter__(self):
            return self

    datapipe = AIDP()
    return datapipe


def test_asynciterdatapipe_repr(datapipe):
    """
    Ensure that the __repr__ method of an AsyncIterDataPipe returns a string
    with the qualified name of the class.
    """
    assert repr(datapipe) == "fixture_datapipe.<locals>.AIDP"
