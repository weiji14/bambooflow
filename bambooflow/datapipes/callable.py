"""
Asynchronous Iterable DataPipes for asynchronous functions.
"""
import asyncio
from collections.abc import AsyncIterator, Callable, Coroutine
from typing import Any

from bambooflow.datapipes.aiter import AsyncIterDataPipe


class MapperAsyncIterDataPipe(AsyncIterDataPipe):
    """
    Applies an asynchronous function over each item from the source DataPipe.

    Parameters
    ----------
    datapipe : AsyncIterDataPipe
        The source asynchronous iterable-style DataPipe.
    fn : Callable
        Asynchronous function to be applied over each item.

    Yields
    ------
    awaitable : collections.abc.Awaitable
        An :py-term:`awaitable` object from the
        :py-term:`asynchronous iterator <asynchronous-iterator>`.

    Raises
    ------
    ExceptionGroup
        If any one of the concurrent tasks raises an :py:class:`Exception`. See
        `PEP654 <https://peps.python.org/pep-0654/#handling-exception-groups>`_
        for general advice on how to handle exception groups.

    Example
    -------
    >>> import asyncio
    >>> from bambooflow.datapipes import AsyncIterableWrapper, Mapper
    ...
    >>> # Apply an asynchronous multiply by two function
    >>> async def times_two(x) -> float:
    ...     await asyncio.sleep(delay=x)
    ...     return x * 2
    >>> dp = AsyncIterableWrapper(iterable=[0.1, 0.2, 0.3])
    >>> dp_map = Mapper(datapipe=dp, fn=times_two)
    ...
    >>> # Loop or iterate over the DataPipe stream
    >>> it = aiter(dp_map)
    >>> number = anext(it)
    >>> asyncio.run(number)
    0.2
    >>> number = anext(it)
    >>> asyncio.run(number)
    0.4
    >>> # Or if running in an interactive REPL with top-level `await` support
    >>> number = anext(it)
    >>> await number  # doctest: +SKIP
    0.6
    """

    def __init__(
        self, datapipe: AsyncIterDataPipe, fn: Callable[..., Coroutine[Any, Any, Any]]
    ):
        super().__init__()
        self._datapipe = datapipe
        self._fn = fn

    async def __aiter__(self) -> AsyncIterator:
        try:
            async with asyncio.TaskGroup() as task_group:
                tasks: list[asyncio.Task] = [
                    task_group.create_task(coro=self._fn(data))
                    async for data in self._datapipe
                ]
        except* BaseException as err:
            raise ValueError(f"{err=}") from err

        for task in tasks:
            result = await task
            yield result
