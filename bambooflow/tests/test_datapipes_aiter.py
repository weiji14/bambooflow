"""
Tests for aiter datapipes.
"""
import pytest

from bambooflow.datapipes import AsyncIterDataPipe, AsyncIterableWrapper


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


async def test_asynciterablewrapper():
    """
    Ensure that AsyncIterableWrapper can wrap an iterable object into an
    AsyncIterDataPipe that yields awaitable objects.
    """
    dp = AsyncIterableWrapper(iterable=range(2))

    # Using aiter/anext
    it = aiter(dp)
    number = await anext(it)
    assert number == 0

    # Using async for-loop, note that datapipe is not reset
    async for number in dp:
        assert number == 1

    # Running beyond the length of the iterable should raise StopAsyncIteration
    with pytest.raises(StopAsyncIteration):
        await anext(it)
