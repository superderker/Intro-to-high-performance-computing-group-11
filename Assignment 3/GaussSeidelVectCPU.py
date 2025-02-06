import numpy as np
from time import perf_counter as time

def gauss_seidel(f):
    newf = np.zeros(f.shape)
    
    newf[1:-1, 1:-1] = 0.25 * ((np.roll(f,1,axis=1)[1:-1, 1:-1]) + 
                            (np.roll(f,-1,axis=1)[1:-1, 1:-1]) +
                            (np.roll(f,1,axis=0)[1:-1, 1:-1]) + 
                            (np.roll(f,-1,axis=0)[1:-1, 1:-1]))
    return newf
    


def setup(x):
    arr=np.random.random((x,x))*1000
    arr[0,:]=0
    arr[:,0]=0
    arr[:,-1]=0
    arr[-1,:]=0
    for i in range(1000):    
        arr = gauss_seidel(arr)

if __name__=="__main__":
    for i in range(100, 210, 10):
        t1=time()
        setup(i)
        print(time()-t1)