"""
Base classes for Asynchronous Iterable DataPipes.
"""
import collections


class AsyncIterDataPipe(collections.abc.AsyncIterable):
    """
    Asynchronous iterable-style DataPipes.

    All DataPipes that represent an asynchronous iterable of data samples
    should subclass this. This style of DataPipes is particularly useful for
    performing I/O-bound tasks such as streaming data from a network disk drive
    or reading multiple files concurrently. ``AsyncIterDataPipe`` is
    initialized in a lazy fashion, and its elements are computed only when
    :py:meth:`__anext__ <object.__anext__>` is called on the async iterator of
    an ``AsyncIterDataPipe``.
    """

    def __repr__(self) -> str:
        # Instead of showing <bamboopipe. ... .AsyncIterableWrapper at 0x.....>,
        # return the class name like <AsyncIterableWrapper>
        return str(self.__class__.__qualname__)
