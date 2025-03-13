import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import h5py as h5
from cupyx.scipy.interpolate import interpn
from time import perf_counter as time
import multiprocessing


"""
multiprocessing
it's better to do multiprocessing for the outer loop instead of fragment data and do multiprocessing for interpn(points,
 datacube, qi, method='linear')
"""


def transferFunction(x):
    exp1 = cp.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = cp.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = cp.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a

def render(i, points, datacube, Nangles):
    print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    # Camera Grid / Query Points -- rotate camera view
    angle = cp.pi / 2 * i / Nangles
    N = 180
    c = cp.linspace(-N / 2, N / 2, N)
    qx, qy, qz = cp.meshgrid(c, c, c)
    qxR = qx
    qyR = qy * cp.cos(angle) - qz * cp.sin(angle)
    qzR = qy * cp.sin(angle) + qz * cp.cos(angle)
    qi = cp.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    
    # Interpolate onto Camera Grid
    camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
    # Do Volume Rendering
    image = cp.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))
    for dataslice in camera_grid:
        r, g, b, a = transferFunction(cp.log(dataslice))
        image[:, :, 0] = a * r + (1 - a) * image[:, :, 0]
        image[:, :, 1] = a * g + (1 - a) * image[:, :, 1]
        image[:, :, 2] = a * b + (1 - a) * image[:, :, 2]
    image = cp.clip(image, 0.0, 1.0)

    # Plot Volume Rendering
    plt.figure(figsize=(4, 4), dpi=80)
    img=image.get()
    plt.imshow(img)
    plt.axis('off')

    # Save figure
    plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.close()
    return img

def simple_projection(datacube):
    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)
    img=cp.log(cp.mean(datacube, 0)).get()
    plt.imshow(img, cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.close()
    return img

def main(test=False):
    """ Volume Rendering """
    #multiprocessing.set_start_method('spawn')
    start=time()
    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = cp.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = cp.linspace(-Nx / 2, Nx / 2, Nx)
    y = cp.linspace(-Ny / 2, Ny / 2, Ny)
    z = cp.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Veiwing Angles
    Nangles = 10
    num_process = 3
    images=[]
    with multiprocessing.Pool(processes=num_process) as pool:
        res=pool.starmap_async(render, [(i, points, datacube, Nangles) for i in range(Nangles)])
        pool.close()
        pool.join()
    simple_proj=simple_projection(datacube)
    print(time()-start)
    if test:
        return res.get(), simple_proj
    return 0
#

if __name__ == "__main__":
    #multiprocessing.set_start_method('spawn')
    main()

