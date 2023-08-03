# API Reference

## Asynchronous-style DataPipes

```{eval-rst}
.. automodule:: bambooflow.datapipes
    :members:
.. autoclass:: bambooflow.datapipes.AsyncIterDataPipe
    :show-inheritance:
.. autoclass:: bambooflow.datapipes.AsyncIterableWrapper
.. autoclass:: bambooflow.datapipes.aiter.AsyncIterableWrapperAsyncIterDataPipe
    :show-inheritance:
```

### Mapping DataPipes

Datapipes which apply a custom asynchronous function to elements in a DataPipe.

```{eval-rst}
.. autoclass:: bambooflow.datapipes.Mapper
.. autoclass:: bambooflow.datapipes.callable.MapperAsyncIterDataPipe
    :show-inheritance:
```
