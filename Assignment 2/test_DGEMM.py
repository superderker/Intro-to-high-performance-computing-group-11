import pytest
import numpy as np
import DGEMM
import random
import array as arr
import time
import matplotlib.pyplot as plt
MAX_VALUE = 10000 # use this?
standard_deviation_list = []
class TestDGEMM:
# run with python3 -m pytest test_DGEMM.py (in virtial env)

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
    def test_np(self, N):
        A = np.random.rand(N, N)
        B = np.random.rand(N, N)
        firstTask = DGEMM.with_np(N, A, B)
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
        
        
        
    
    # @pytest.mark.parametrize(
    #     "N",
    #     [
    #         (1), 
    #         (11),   
    #         (21),
    #         (31),
    #         (41),
    #         (51),
    #         (61),
    #         (71),
    #         (81),
    #         (91),
    #         (200),
    #         (300),
    #         (400),
    #         (500),
    #         (600),
    #         (700),
    #         (800),
    #         (900),
    #         (1000)
    #     ]
    # )
    # # python3 -m pytest -s test_DGEMM.py lets you see the time 

    # def test_np_with_timer(self, N):
        
    #     A = np.random.rand(N, N)
    #     B = np.random.rand(N, N)
    #     t1 = time.perf_counter()
    #     firstTask = DGEMM.with_np(N, A, B)
    #     t2 = time.perf_counter()
    #     tFinal = t2 - t1
    #     print("time for matrix ", N ,"X", N, " = ",  tFinal * 1000, "ms")
    #     expected = np.dot(A, B)
        
    #     assert np.allclose(firstTask, expected)
    @pytest.mark.parametrize(
        "N",
        [ 
            (10),   
            (20),
            (30),
            (40),
            (50),
            (60),
            (70),
            (80),
            (90),
            (100)
        ]
    )
    def test_np_with_timer_gather_std(self, N, iter=3):
        res = []
        for i in range(iter):
            A = np.random.rand(N, N)
            B = np.random.rand(N, N)
            t1 = time.perf_counter()
            firstTask = DGEMM.with_np(N, A, B)
            t2 = time.perf_counter()
            tFinal = (t2 - t1) * 1000
            print("time for matrix ", N ,"X", N, " = ",  tFinal, "ms")
            res.append(tFinal)
            expected = np.dot(A, B)
        standard_each_loop = np.std(res)
        standard_deviation_list.append(standard_each_loop)
            
        assert np.allclose(firstTask, expected)
    
    def test_standard_deviation(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
        std_list_as_floats = [float(std) for std in standard_deviation_list]
        
        print("std list: ", std_list_as_floats)

        # 🔹 Plot standard deviation vs. matrix size
        plt.figure(figsize=(8, 5))
        plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='b', label="Standard Deviation")

        # 🔹 Labels & Title
        plt.xlabel("Matrix Size (N)")
        plt.ylabel("Standard Deviation (ms)")
        plt.title("Standard Deviation of Execution Time vs. Matrix Size")
        plt.legend()
        plt.grid(True)

        # 🔹 Show Plot
        plt.show()
