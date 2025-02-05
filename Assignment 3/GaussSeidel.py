import numpy as np
from time import perf_counter as time

def gauss_seidel(f):
    newf = f.copy()
    
    for i in range(1,newf.shape[0]-1):
        for j in range(1,newf.shape[1]-1):
            newf[i,j] = 0.25 * (newf[i,j+1] + newf[i,j-1] +
                                   newf[i+1,j] + newf[i-1,j])
    
    return newf


def setup(x):
    arr=np.random.random((x,x))*1000
    arr[0,:]*=0
    arr[:,0]*=0
    arr[:,x-1]*=0
    arr[x-1,:]*=0
    for i in range(1000):    
        arr = gauss_seidel(arr)

if __name__=="__main__":
    #setup(100)
    for i in range(100, 210, 10):
        t1=time()
        setup(i)
        print(time()-t1)