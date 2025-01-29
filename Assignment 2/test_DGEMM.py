import pytest
import numpy as np
import DGEMM
import random
import array as arr
MAX_VALUE = 10000 # use this?
class TestDGEMM:
# run with python3 -m pytest test_DGEMM.py (in virtial env)

    @pytest.mark.parametrize(
        "N",
        [
            (1),  # Example: original test case
            (11),   # Example: idk what to put to make it work
            (21),
            (31),
            (41),
            (51),
            (61),
            (71),
            (81),
            (91)
        ]
    )
    def test_np(self, N):
        A = np.random.rand(N, N)
        B = np.random.rand(N, N)
        firstTask = DGEMM.with_np(N, A, B)
        expected = np.dot(A, B)
        assert np.allclose(firstTask, expected)
    @pytest.mark.parametrize(
        "N",
        [
            (1),  # Example: original test case
            (11),   # Example: idk what to put to make it work
            (21),
            (31),
            (41),
            (51),
            (61),
            (71),
            (81),
            (91)
        ]
    )
    def test_lists(self, N):
        A = [[random.randint(0, N) for _ in range(N)] for _ in range(N)]
        B = [[random.randint(0, N) for _ in range(N)] for _ in range(N)]
        firstTask = DGEMM.with_lists(N, A, B)
        expected = np.dot(A, B)
        assert np.allclose(firstTask, expected)
    
    @pytest.mark.parametrize(
        "N",
        [
            (1),  
            (11),   
            (21),
            (31),
            (41),
            (51),
            (61),
            (71),
            (81),
            (91)
        ]
    ) 
    def test_arrays(self, N):
        A = [arr.array('i', [random.randint(0, N) for _ in range(N)]) for _ in range(N)]
        B = [arr.array('i', [random.randint(0, N) for _ in range(N)]) for _ in range(N)]
        firstTask = DGEMM.with_arrays(N, A, B)
        expected = np.dot(A, B)
        assert np.allclose(firstTask, expected)
    