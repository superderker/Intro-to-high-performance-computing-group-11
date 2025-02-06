import pytest
import numpy as np
import DGEMM
import random
import array as arr
import time
import matplotlib.pyplot as plt
MAX_VALUE = 10000 # use this?
std_dev_list=[]
std_dev_arr=[]
std_dev_np = []
mean_list_list = []
mean_arr_list = []
mean_dot_list = []
mat_mul_list = []
mean_mat_mul_list = []
flops_list = []
flops_per_second_list=[]
flops_list_res = []
flops_arr_res = []
flops_per_second_list_list=[]
flops_per_second_arr_list=[]
flops = 0
class TestDGEMM:
# run with python3 -m pytest test_DGEMM.py (in virtial env)
# python3 -m pytest -s test_DGEMM.py lets you see the time
# 
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
        C = np.random.rand(N, N)
        firstTask = DGEMM.with_np(N, A, B, C)
        expected = C + np.dot(A, B)
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
        A = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]
        B = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]
        C = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]
        C_np = np.array(C)
        expected = C_np + np.dot(A, B)
        firstTask = DGEMM.with_lists(N, A, B, C)
        firstTask_np = np.array(firstTask)
        assert np.allclose(firstTask_np, expected)

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
        A = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]
        B = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]
        C = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]  
        C_np = np.array(C, dtype=np.float64)
        expected = C_np + np.dot(np.array(A, dtype=np.float64), np.array(B, dtype=np.float64)) 
        firstTask = DGEMM.with_arrays(N, A, B, C)
        firstTask_np = np.array(firstTask, dtype=np.float64)
        assert np.allclose(firstTask_np, expected)

        
        
    
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
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    )
    def test_list_with_timer_gather_std(self, N, iter=10):
        res = []
        for i in range(iter):
            # Generate random matrices
            A = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]
            B = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]
            C = [[random.uniform(0, N) for _ in range(N)] for _ in range(N)]  

            C_np = np.array(C)
            expected = C_np + np.dot(A, B)  

            # Time the multiplication
            t1 = time.perf_counter()
            firstTask = DGEMM.with_lists(N, A, B, C)
            t2 = time.perf_counter()

            tFinal = (t2 - t1) * 1000  # Convert to ms
            print("time for matrix ", N ,"X", N, " = ",  tFinal, "ms")
            res.append(tFinal)

            # Convert firstTask to NumPy for correct comparison
            firstTask_np = np.array(firstTask)
            assert np.allclose(firstTask_np, expected)

        flops = 2 * (N ** 3)/(10**9)
        flops_list_res.append(flops)
        standard_each_loop = np.std(res)
        mean_list_list.append(np.mean(res))
        flops_per_second_list_list.append((1000* flops) / np.mean(res))# back to seconds
        std_dev_list.append(standard_each_loop)

    @pytest.mark.parametrize(
        "N",
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    )
    def test_arr_with_timer_gather_std(self, N, iter=10):
        res = []
        for i in range(iter):
            A = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]
            B = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]
            C = [arr.array('d', [random.uniform(0, N) for _ in range(N)]) for _ in range(N)]  
            
            C_np = np.array(C, dtype=np.float64)
            expected = C_np + np.dot(np.array(A, dtype=np.float64), np.array(B, dtype=np.float64))

            t1 = time.perf_counter()
            firstTask= DGEMM.with_arrays(N, A, B, C)
            t2 = time.perf_counter()

            tFinal = (t2 - t1) * 1000  # Convert to ms
            print("time for matrix ", N ,"X", N, " = ",  tFinal, "ms")
            res.append(tFinal)
            firstTask_np = np.array(firstTask, dtype=np.float64)
            assert np.allclose(firstTask_np, expected)

        flops = 2 * (N ** 3)/(10**9)    
        flops_arr_res.append(flops)
        standard_each_loop = np.std(res)
        mean_each_loop = np.mean(res)
        std_dev_arr.append(standard_each_loop)
        flops_per_second_arr_list.append((1000* flops) / np.mean(res))# back to seconds
        mean_arr_list.append(mean_each_loop)
        

    @pytest.mark.parametrize(
        "N",
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    )
    def test_np_with_timer_gather_std(self, N, iter=10):
        res = []
        for i in range(iter):
            A = np.random.rand(N, N)
            B = np.random.rand(N, N)
            C = np.random.rand(N, N)  
            
            expected = C + np.dot(A, B)
            t1 = time.perf_counter()
            firstTask = DGEMM.with_np(N, A, B, C)
            t2 = time.perf_counter()

            tFinal = (t2 - t1) * 1000  # Convert to ms
            print("time for matrix ", N ,"X", N, " = ",  tFinal, "ms")
            res.append(tFinal)
            

            assert np.allclose(firstTask, expected)

        flops = 2 * (N ** 3)/(10**9)
        flops_list_res.append(flops)
        standard_each_loop = np.std(res)
        mean_each_loop = np.mean(res)
        std_dev_np.append(standard_each_loop)
        flops_per_second_list.append((1000* flops) / np.mean(res))# back to seconds
        mean_dot_list.append(mean_each_loop)

    @pytest.mark.parametrize(
        "N",
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    )
    def test_np_with_timer_gather_std_mat_mul(self, N, iter=10):
        res = []
        for i in range(iter):
            A = np.random.rand(N, N)
            B = np.random.rand(N, N)
            C = np.random.rand(N, N)  
            
            expected = C + np.dot(A, B)

            t1 = time.perf_counter()
            firstTask = DGEMM.with_matmul(N, A, B, C)
            t2 = time.perf_counter()

            tFinal = (t2 - t1) * 1000  # Convert to ms
            res.append(tFinal)

            assert np.allclose(firstTask, expected)

        standard_each_loop = np.std(res)
        mean_mat_mul_list.append(np.mean(res))
        mat_mul_list.append(standard_each_loop)

    def test_compare_times_all(self):
        std_mat_mul = [float(std) for std in mat_mul_list]
        std_arr = [float(std) for std in std_dev_arr]
        std_list = [float(std) for std in std_dev_list]
        std_np = [float(std) for std in std_dev_np]

        for i in range(len(std_list)):
            print(f"With lists: {std_list[i]:.6f} ms, with arrays: {std_arr[i]:.6f} ms, np.dot: {std_np[i]:.6f} ms, matmul: {std_mat_mul[i]:.6f} ms")
            
            all_stds = {
                "lists": std_list[i],
                "arrays": std_arr[i],
                "np.dot": std_np[i],
                "matmul": std_mat_mul[i]

            }
            smallest = min(all_stds, key=all_stds.get)
            print(f"Smallest: {all_stds[smallest]:.6f} ms from {smallest}")

    def test_standard_deviation_mat_mul(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
        std_list_as_floats = [float(std) for std in mean_mat_mul_list]

        plt.figure(figsize=(8, 5))
        plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='y', label="Standard Deviation for mat mul (task 2.5)")

        plt.xlabel("Matrix Size (N)")
        plt.ylabel("Standard Deviation (ms)")
        plt.title("Standard Deviation of Execution Time vs. Matrix Size")
        plt.legend()
        plt.grid(True)
        plt.show()
    def test_mean_mat_mul(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
        std_list_as_floats = [float(std) for std in mat_mul_list]

        plt.figure(figsize=(8, 5))
        plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='y', label="mean for mat mul (task 2.5)")

        plt.xlabel("Matrix Size (N)")
        plt.ylabel("mean (ms)")
        plt.title("mean of Execution Time vs. Matrix Size")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    # def test_standard_deviation_lists(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
    #     std_list_as_floats = [float(std) for std in mean_list_list]
    #     plt.figure(figsize=(8, 5))
    #     plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='r', label="Mean for lists")
    #     plt.xlabel("Matrix Size (N)")
    #     plt.ylabel("Mean (ms)")
    #     plt.title("Mean of Execution Time vs. Matrix Size")
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()

    # def test_standard_deviation_arrays(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
    #     std_list_as_floats = [float(std) for std in mean_arr_list]
    #     plt.figure(figsize=(8, 5))
    #     plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='g', label="Mean for arrays")
    #     plt.xlabel("Matrix Size (N)")
    #     plt.ylabel("mean (ms)")
    #     plt.title("Mean of Execution Time vs. Matrix Size")
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()
        
        
    # def test_standard_deviation(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
    #     std_list_as_floats = [float(std) for std in mean_dot_list]
    #     plt.figure(figsize=(8, 5))
    #     plt.plot(N_list, std_list_as_floats, marker='o', linestyle='-', color='b', label="Mean for np.dot")
    #     plt.xlabel("Matrix Size (N)")
    #     plt.ylabel("Mean time (ms)")
    #     plt.title("Mean of Execution Time vs. Matrix Size")
    #     plt.legend()
    #     plt.grid(True)
    #     plt.show()
        
    # def test_standard_deviation_of_flops(self, N_list=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
    #     print("flops list", flops_list)
    #     print("--------------------------------------------")
    #     print("flops per second: ", flops_per_second_list)
    #     print("--------------------------------------------")
    #     print("flops list res: ", flops_list_res)
    #     print("--------------------------------------------")
    #     print("flops arr res: ", flops_arr_res)
    #     print("--------------------------------------------")
    #     print("flops per second list list: ", flops_per_second_list_list)
    #     print("--------------------------------------------")
    #     print("flops per second arr list: ", flops_per_second_arr_list)
