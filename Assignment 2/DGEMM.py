# Multiplying first and second matrices and storing it in result
#    for (int i = 0; i < N; ++i) {
#       for (int j = 0; j < N; ++j) {
#          for (int k = 0; k < N; ++k) {
#             C[i][j] = C[i][j] + A[i][k] * B[k][j];
#          }
#       }
#    }

def with_lists(N, A, B):
    C = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    return C
import array as arr
def with_arrays(N, A, B):
    
    C = [arr.array('i', [0] * N) for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    
    return C
# task 2.1 
import numpy as np
def with_np_slow(N, A, B):

    C = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C
def with_np(N, A, B):

    C = np.zeros((N, N))

    C = np.dot(A,B)
    return C

def with_np_slow_and_flops(N, A, B):

    C = np.zeros((N, N))   
    flops = 0

    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
                flops += 1
    return C, flops

def with_np_and_flops(N, A, B):

    C = np.zeros((N, N))

    C = np.dot(A,B)
    flops = (2*(N**3))
    return C, flops
# Task 2.5 Compare the performance results with the numpy matmul operation (that uses a BLAS library). 
def with_matmul(N, A, B):
    C = np.matmul(A, B)
    return C


