"""
Tests for callable datapipes.
"""
import asyncio
import time
from collections.abc import Awaitable

import pytest

from bambooflow.datapipes import AsyncIterableWrapper, Mapper


# %%
@pytest.fixture(scope="function", name="times_two")
def fixture_times_two():
    async def times_two(x) -> int:
        await asyncio.sleep(0.2)
        print(f"Multiplying {x} by 2")
        result = x * 2
        return result

    return times_two


@pytest.fixture(scope="function", name="times_three")
def fixture_times_three():
    async def times_three(x) -> int:
        await asyncio.sleep(0.3)
        print(f"Multiplying {x} by 3")
        result = x * 3
        return result

    return times_three


async def test_mapper(times_two, times_three):
    """
    Ensure that MapperAsyncIterDataPipe works to process tasks concurrently,
    such that three tasks taking 3*(0.2+0.3)=1.5 seconds in serial can be
    completed in just (0.2+0.3)=0.5 seconds instead.
    """
    dp = AsyncIterableWrapper(iterable=[0, 1, 2])
    dp_map2 = Mapper(datapipe=dp, fn=times_two)
    dp_map3 = Mapper(datapipe=dp_map2, fn=times_three)

    i = 0
    tic = time.perf_counter()
    async for num in dp_map3:
        # print("Number:", num)
        assert num == i * 2 * 3
        toc = time.perf_counter()
        i += 1
        # print(f"Ran in {toc - tic:0.4f} seconds")
    print(f"Total: {toc - tic:0.4f} seconds")

    assert toc - tic < 0.55  # Total time should be about 0.5 seconds
    assert num == 12  # 2*2*3=12
