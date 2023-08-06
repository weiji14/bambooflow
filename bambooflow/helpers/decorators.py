"""
Decorators to wrap around DataPipe classes.
"""
import functools

from bambooflow.datapipes.aiter import AsyncIterDataPipe


class functional_datapipe:
    """
    Decorator to wrap an ``AsyncIterDataPipe`` to have a functional form.

    Parameters
    ----------
    name : str
        The name for the functional form of the
        :py:class:`bambooflow.datapipes.AsyncIterDataPipe`.

    Note
    ----
    The functional method is injected into the private ``_functions`` variable
    of the base ``AsyncIterDataPipe`` class, and relies on the modified
    ``AsyncIterDataPipe.__getattr__`` method to call the wrapped function.

    Example
    -------
    >>> from bambooflow.datapipes import AsyncIterableWrapper
    >>> from bambooflow.helpers import functional_datapipe
    >>>
    >>> @functional_datapipe(name="pipe")
    ... class PiperAsyncIterDataPipe(AsyncIterDataPipe):
    ...     def __init__(self, datapipe):
    ...         ...
    ...     async def __aiter__(self):
    ...         ...
    >>>
    >>> dp = AsyncIterableWrapper(iterable=["a", "b", "c"])
    >>> dp_pipe = dp.pipe()
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, cls, *args, **kwargs) -> AsyncIterDataPipe:
        def class_function(source_dp, *args, **kwargs):
            return cls(source_dp, *args, **kwargs)

        function = functools.partial(class_function, *args, **kwargs)
        functools.update_wrapper(wrapper=function, wrapped=cls, assigned=("__doc__",))

        # Set function/method on base AsyncIterDataPipe, so that all classes
        # inheriting from AsyncIterDataPipe can use the function too
        AsyncIterDataPipe._functions[self.name] = function

        return cls
