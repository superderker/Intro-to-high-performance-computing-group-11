import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import timeit
import multiprocessing
from multiprocessing import shared_memory
# from memory_profiler import profile


"""
multiprocessing
it's better to do multiprocessing for the outer loop instead of fragment data and do multiprocessing for interpn(points,
 datacube, qi, method='linear')
"""

SHARED_MEM_NAME = "datacube_shared"


def transferFunction(x):
    exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a

def render(i, points, shape, dtype, shared_mem_name, Nangles):
    print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')

    existing_shm = shared_memory.SharedMemory(name=shared_mem_name)
    datacube = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

    # Camera Grid / Query Points -- rotate camera view
    angle = np.pi / 2 * i / Nangles
    N = 180
    c = np.linspace(-N / 2, N / 2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle)
    qzR = qy * np.sin(angle) + qz * np.cos(angle)
    qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T

    # Interpolate onto Camera Grid
    camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))

    # Do Volume Rendering
    image = np.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))

    for dataslice in camera_grid:
        r, g, b, a = transferFunction(np.log(dataslice))
        image[:, :, 0] = a * r + (1 - a) * image[:, :, 0]
        image[:, :, 1] = a * g + (1 - a) * image[:, :, 1]
        image[:, :, 2] = a * b + (1 - a) * image[:, :, 2]

    image = np.clip(image, 0.0, 1.0)

    # Plot Volume Rendering
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(image)
    plt.axis('off')

    # Save figure
    plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.close()
    existing_shm.close()
    return image

def simple_projection(shape, dtype, shared_mem_name):
    # Plot Simple Projection -- for Comparison
    existing_shm = shared_memory.SharedMemory(name=shared_mem_name)
    datacube = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

    plt.figure(figsize=(4, 4), dpi=80)
    proj=np.log(np.mean(datacube, 0))
    plt.imshow(proj, cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()
    plt.close()

    existing_shm.close()
    return proj
# @profile
def main(test=False):
    """ Volume Rendering """

    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = np.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx / 2, Nx / 2, Nx)
    y = np.linspace(-Ny / 2, Ny / 2, Ny)
    z = np.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Create Shared Memory
    shm = shared_memory.SharedMemory(create=True, size=datacube.nbytes, name=SHARED_MEM_NAME)
    shared_datacube = np.ndarray(datacube.shape, dtype=datacube.dtype, buffer=shm.buf)
    shared_datacube[:] = datacube[:]  # Copy the data to shared memory

    # Do Volume Rendering at Different Veiwing Angles
    Nangles = 10
    num_process = 10
    with multiprocessing.Pool(processes=num_process) as pool:
        res=pool.starmap(render, [(i, points, datacube.shape, datacube.dtype, SHARED_MEM_NAME, Nangles) for i in range(Nangles)])
        simple_proj=pool.apply(simple_projection, args=(datacube.shape, datacube.dtype, SHARED_MEM_NAME))
        pool.close()
        pool.join()

    shm.close()
    shm.unlink()
    if test:
        return res, simple_proj
    return 0
#

if __name__ == "__main__":
    main()

