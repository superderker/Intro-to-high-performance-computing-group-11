import cupy as cp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import h5py as h5
from cupyx.scipy.interpolate import interpn
from time import perf_counter as time
from memory_profiler import profile
from dask import delayed
from dask.distributed import Client
import dask.array as da
import dask
import numpy as np


"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""


def transferFunction(x):
    exp1 = cp.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = cp.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = cp.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r,g,b,a

def interpolate_block(datacube, points, qi):
    # print("interpolate_block", qi.shape)
    return interpn(points, datacube, qi, method='linear')

# @delayed
def render(i, points, datacube, Nangles):
    print('Rendering Scene ' + str(i+1) + ' of ' + str(Nangles) + '.\n')

    # Camera Grid / Query Points -- rotate camera view
    angle = cp.pi/2 * i / Nangles
    N = 180
    c = cp.linspace(-N/2, N/2, N)
    qx, qy, qz = cp.meshgrid(c,c,c)
    qxR = qx
    qyR = qy * cp.cos(angle) - qz * cp.sin(angle) 
    qzR = qy * cp.sin(angle) + qz * cp.cos(angle)
    qi = cp.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    qi = da.from_array(qi, chunks=(N * N, 3))

    # Interpolate onto Camera Grid
    camera_grid_future = da.map_blocks(interpolate_block, datacube, points, qi, dtype='float64', chunks=(qi.chunks[0],)
                                       , drop_axis=1)
    camera_grid = camera_grid_future.compute()
    camera_grid = camera_grid.reshape((N, N, N))

    # Do Volume Rendering
    image = cp.zeros((camera_grid.shape[1],camera_grid.shape[2],3))

    for dataslice in camera_grid:
        r,g,b,a = transferFunction(cp.log(dataslice))
        image[:,:,0] = a*r + (1-a)*image[:,:,0]
        image[:,:,1] = a*g + (1-a)*image[:,:,1]
        image[:,:,2] = a*b + (1-a)*image[:,:,2]

    image = cp.clip(image,0.0,1.0)

    # Plot Volume Rendering
    plt.figure(figsize=(4,4), dpi=80)
    img=image.get()
    plt.imshow(img)
    plt.axis('off')

    # Save figure
    plt.savefig('volumerender' + str(i) + '.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
    plt.close()
    return img 

@delayed
def simple_projection(datacube):
    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4,4), dpi=80)
    plotData=cp.asnumpy(cp.log(cp.mean(datacube,0)))
    plt.imshow(plotData, cmap = 'viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
    plt.close()
    return plotData

# @profile
def main(angles=10, test=False):
    """ Volume Rendering """
    start=time()

    # Start Dask Client
    client = Client(n_workers=8)
    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = cp.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = cp.linspace(-Nx/2, Nx/2, Nx)
    y = cp.linspace(-Ny/2, Ny/2, Ny)
    z = cp.linspace(-Nz/2, Nz/2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Viewing Angles
    Nangles = angles
    images=[]
    for i in range(Nangles):
        if test:
            images.append(render(i, points, datacube, Nangles))
        else:
            render(i, points, datacube, Nangles)
    res=dask.compute(simple_projection(datacube))
    client.close()
    if test:
        simple_proj=list(res[0])
        return images, simple_proj
    return time()-start


if __name__ == "__main__":
    with open("runtime NVIDIA/daskgpu.txt", "w", buffering=1) as f:
        for i in range(1,6):
            runs=[]
            for x in range(1,4):
                runs.append(main(angles=i*10))
            f.write(f"{i*10}: {np.mean(runs)}, {np.std(runs)} \n") 

