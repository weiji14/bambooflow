"""
An asynchronous-style DataPipe is one that implements the
:py:meth:`__aiter__ <object.__aiter__>` protocol, and represents an
:py-term:`asynchronous iterable <asynchronous-iterable>` over data samples.
This is well-suited for cases when I/O latency is slow, e.g. when waiting on
network connections, or performing read operations on multiple files at once.
"""

from bambooflow.datapipes.aiter import (
    AsyncIterDataPipe,
    AsyncIterableWrapperAsyncIterDataPipe as AsyncIterableWrapper,
)
from bambooflow.datapipes.callable import MapperAsyncIterDataPipe as Mapper
