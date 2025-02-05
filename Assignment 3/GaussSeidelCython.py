import numpy as np
from time import perf_counter as time
import cythonfnOpt
import cythonfn

def setup(x, ver):
    arr=np.random.random((x,x))*100000000
    arr[0,:]*=0
    arr[:,0]*=0
    arr[:,x-1]*=0
    arr[x-1,:]*=0
    if ver==0:
        for i in range(1000):    
            arr = cythonfnOpt.gauss_seidel(arr)
    else:
        for i in range(1000):    
            arr = cythonfn.gauss_seidel(arr)


if __name__=="__main__":
    print("Cython with type definition and memoryviews")
    for i in range(100, 210, 10):
        t1=time()
        setup(i,0)
        print(f"{time()-t1} seconds for {i}x{i} grid",)
    print("Cython without modifications")
    for i in range(100, 210, 10):
        t1=time()
        setup(i,1)
        print(f"{time()-t1} seconds for {i}x{i} grid",)