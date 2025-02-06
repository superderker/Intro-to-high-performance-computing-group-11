import cupy as cp
import torch as tc
from time import perf_counter as time

def gauss_seidelPytorch(f):
    newf = tc.zeros(f.shape).cuda()
    
    newf[1:-1, 1:-1] = 0.25 * ((tc.roll(f,1,dims=1)[1:-1, 1:-1]) + 
                            (tc.roll(f,-1,dims=1)[1:-1, 1:-1]) +
                            (tc.roll(f,1,dims=0)[1:-1, 1:-1]) + 
                            (tc.roll(f,-1,dims=0)[1:-1, 1:-1]))
    return newf

def gauss_seidelCuPy(f):
    newf = cp.zeros(f.shape)
    
    newf[1:-1, 1:-1] = 0.25 * ((cp.roll(f,1,axis=1)[1:-1, 1:-1]) + 
                            (cp.roll(f,-1,axis=1)[1:-1, 1:-1]) +
                            (cp.roll(f,1,axis=0)[1:-1, 1:-1]) + 
                            (cp.roll(f,-1,axis=0)[1:-1, 1:-1]))
    return newf
    
    


def setupPytorch(x):
    arr=(tc.randint(1000, (x,x))).cuda()
    arr[0,:]=0
    arr[:,0]=0
    arr[:,-1]=0
    arr[-1,:]=0
    for i in range(1000):    
        arr = gauss_seidelPytorch(arr)
    tc.cuda.synchronize()

def setupCuPy(x):
    arr=(cp.random.random((x,x))*1000)
    arr[0,:]=0
    arr[:,0]=0
    arr[:,-1]=0
    arr[-1,:]=0
    for i in range(1000):    
        arr = gauss_seidelCuPy(arr)
    cp.cuda.Stream.null.synchronize()

if __name__=="__main__":
    print("Pytorch:")
    for i in range(100, 210, 10):
        t1=time()
        setupPytorch(i)
        print(f"{time()-t1} seconds for {i}x{i} gridsize")
    print("CuPy:")
    for i in range(100, 210, 10):
        t1=time()
        setupCuPy(i)
        print(f"{time()-t1} seconds for {i}x{i} gridsize")