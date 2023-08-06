"""
Asynchronous Iterable DataPipes base class and wrapper.
"""
import functools
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable, Iterable


class AsyncIterDataPipe(AsyncIterable):
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

    _functions: dict[str, Callable] = {}

    def __getattr__(self, attribute_name: str) -> Callable:
        """
        Allow calling functions stored in the private ``_functions`` variable,
        e.g. those added by the functional_datapipe decorator.
        """
        if f := AsyncIterDataPipe._functions.get(attribute_name):
            function = functools.partial(f, self)
            functools.update_wrapper(wrapper=function, wrapped=f, assigned=("__doc__",))
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attribute_name}'"
            )
        return function

    def __repr__(self) -> str:
        # Instead of showing <bambooflow. ... .AsyncIterableWrapper at 0x.....>,
        # return the qualified name of the class like <AsyncIterableWrapper>
        return str(self.__class__.__qualname__)


class AsyncIterableWrapperAsyncIterDataPipe(AsyncIterDataPipe):
    """
    Wraps an iterable object to create an AsyncIterDataPipe.

    Adapted from https://peps.python.org/pep-0492/#example-2

    Parameters
    ----------
    iterable : collections.abc.Iterable
        An :py-term:`iterable` object to be wrapped into an AsyncIterDataPipe.

    Yields
    ------
    awaitable : collections.abc.Awaitable
        An :py-term:`awaitable` object from the
        :py-term:`asynchronous iterator <asynchronous-iterator>`.

    Example
    -------
    >>> import asyncio
    >>> from bambooflow.datapipes import AsyncIterableWrapper
    ...
    >>> # Wrap a list into an asynchronous iterator
    >>> dp = AsyncIterableWrapper(iterable=[3, 6, 9])
    ...
    >>> # Loop or iterate over the DataPipe stream
    >>> it = aiter(dp)
    >>> number = anext(it)
    >>> asyncio.run(number)
    3
    >>> number = anext(it)
    >>> asyncio.run(number)
    6
    >>> # Or if running in an interactive REPL with top-level `await` support
    >>> number = anext(it)  # doctest: +SKIP
    >>> await number  # doctest: +SKIP
    9
    """

    def __init__(self, iterable: Iterable):
        self._iterable = iter(iterable)

    def __aiter__(self) -> AsyncIterator:
        return self

    async def __anext__(self) -> Awaitable:
        try:
            value = next(self._iterable)
        except StopIteration as err:
            raise StopAsyncIteration from err
        return value
