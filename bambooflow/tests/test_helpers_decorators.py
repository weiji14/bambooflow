"""
Test the helper function/class decorators used to build DataPipes.
"""
import pydoc

import pytest

from bambooflow.datapipes import AsyncIterableWrapper, AsyncIterDataPipe
from bambooflow.helpers.decorators import functional_datapipe


# %%
def test_functional_datapipe_wrapper():
    """
    Ensure that the functional_datapipe decorator works to inject a new method
    into an AsyncIterDataPipe.
    """

    @functional_datapipe(name="flow")
    class FlowerAsyncIterDataPipe(AsyncIterDataPipe):
        pass

    dp = AsyncIterableWrapper(iterable=range(5))
    assert hasattr(dp, "flow")  # Check that new 'flow' method can be called


@pytest.mark.parametrize("funcname", ["map"])
def test_functional_form_docstring(funcname):
    """
    Ensure that the functional form of an AsyncIterDataPipe has the correct
    docstring from the class form.
    """
    dp = AsyncIterableWrapper(iterable=range(5))

    docstring = pydoc.render_doc(thing=getattr(dp, funcname))
    assert f"(functional name: ``{funcname}``)" in docstring
    assert "Parameters\n    ----------" in docstring
    assert "Yields\n    ------" in docstring
    assert "Example\n    -------" in docstring
