import os

import numpy as np
from time import perf_counter as time
import h5py

filename = "newgrid_results.hdf5"

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

    # store the result to HDF5 file
    with h5py.File(filename, "a") as f:
        dataset_name = f"{x}x{x}/newgrid"
        dset = f.create_dataset(dataset_name, data=arr)
        dset.attrs["grid_size"] = x
        dset.attrs["iterations"] = 1000
        dset.attrs["description"] = f"Gauss-Seidel result for {x}x{x} grid"

    print(f"Saved {x}x{x} grid to {filename} under dataset '{dataset_name}'")

if __name__=="__main__":
    if os.path.exists(filename):
        os.remove(filename)

    # You can adjust this to any desired size for storage
    # Modify this to customize the size
    for i in range(100, 210, 10):
        t1=time()
        setup(i)
        print(f"{time()-t1} seconds for {i} x {i} grid")