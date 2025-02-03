import pytest
import numpy as np
import DGEMM
import random
import array as arr
import time
import matplotlib.pyplot as plt
MAX_VALUE = 10000 # use this?
standard_deviation_list = []
flops_list = []
flops_per_second_list=[]
flops = 0
class TestDGEMM:
# run with python3 -m pytest test_DGEMM.py (in virtial env)
# python3 -m pytest -s test_DGEMM.py lets you see the time

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
    #  

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
    def test_np_with_timer_gather_std(self, N, iter=10):
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
        
        # print("std list: ", std_list_as_floats)

        
        plt.figure(figsize=(8, 5))
        plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='b', label="Standard Deviation")

        
        plt.xlabel("Matrix Size (N)")
        plt.ylabel("Standard Deviation (ms)")
        plt.title("Standard Deviation of Execution Time vs. Matrix Size")
        plt.legend()
        plt.grid(True)

        
    
        plt.show()
        
        




        
    
        plt.show()

# task 2.4
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
    def test_np_with_timer_gather_std(self, N, iter=10):
        res = []
        flops_res=[]
        flops = 0
        for i in range(iter):
            A = np.random.rand(N, N)
            B = np.random.rand(N, N)
            t1 = time.perf_counter()
            firstTask, flops = DGEMM.with_np_and_flops(N, A, B)
            t2 = time.perf_counter()
            tFinal = (t2 - t1) * 1000
            print("time for matrix ", N ,"X", N, " = ",  tFinal, "ms")

            res.append(tFinal)
            
        
            expected = np.dot(A, B)
        standard_each_loop = np.std(res)
        standard_deviation_list.append(standard_each_loop)
        print("flops: ", flops)
        flops_list.append(flops_res)# always the same anyway
        flops_res.append(flops)
        flops_per_second=float(flops/standard_each_loop)*1000000    # I think this is right since timer is in ns
        flops_per_second_list.append(flops_per_second)
        assert np.allclose(firstTask, expected)
        
        
    def test_standard_deviation_of_flops(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
        print("flops list", flops_list)
        print("--------------------------------------------")
        print("flops per second: ", flops_per_second_list)

# Clock frequency = f (GHz)
# Number of cores = C
# Floating-point operations per cycle per core = I (depends on SIMD capabilities, e.g., AVX, AVX-512)
# Peak FLOPS=f×C×I
# according to google my computer has f = 3.2 Ghz, C=4 (there are more cores but only 4 should be used by python), I=8 flops/cycle
# = 102.4 Gflops/second which is way less than i got(wtf?)