import pytest
import numpy as np
from volumerender import main as real
from volumerender_mp import main as mp
from volumerender_dask import main as dask
from volumerender_daskAndmp import main as daskMp
from volumerender_dask2 import main as dask2
from volumerender_numba import main as numba
from volumerender_python import main as python
from volumerender_cupy import main as cupy
from volumerender_cupyAndmp import main as cupyMp
from volumerender_daskAndcupy import main as cupyDask
from volumerender_daskAndGPU import main as daskGPU

class TestVolumeRender:
    expectedFrames=[]
    expectedSimpleProjection=[]

    @pytest.fixture(autouse=True, scope="session")
    def setup_and_teardown(self):
        global expectedFrames
        global expectedSimpleProjection
        expectedFrames, expectedSimpleProjection=real(test=True)
        yield
    @pytest.mark.parametrize(
        "func",
        [ 
            numba,
            python,
            mp,
            daskMp,
            dask,
            dask2,
            daskGPU,
            cupy,
            cupyMp,
            cupyDask
        ]
    )
    def test_validate(self, func):
        actualFrames, actualSimpleProjection = func(test=True)
        print(type(actualSimpleProjection))
        assert np.allclose(actualSimpleProjection, expectedSimpleProjection, rtol=1e-04, atol=1e-05)
        for x in range(len(actualFrames)):
            print(f"frame{x}")
            assert np.allclose(actualFrames[x], expectedFrames[x])