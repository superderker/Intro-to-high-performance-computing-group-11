import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import timeit
from memory_profiler import profile
from dask import delayed
from dask.distributed import Client
import dask.array as da
import dask


"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""


def transferFunction(x):
    exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a

def interpolate_block(datacube, points, qi):
    print("interpolate_block", qi.shape)
    return interpn(points, datacube, qi, method='linear')

# @delayed
def render(i, points, datacube, Nangles):
    print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')

    # Camera Grid / Query Points -- rotate camera view
    angle = np.pi / 2 * i / Nangles
    N = 180
    c = np.linspace(-N / 2, N / 2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle)
    qzR = qy * np.sin(angle) + qz * np.cos(angle)
    qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T

    qi = da.from_array(qi, chunks=(N * N, 3))

    # Interpolate onto Camera Grid
    camera_grid_future = da.map_blocks(interpolate_block, datacube, points, qi, dtype='float64', chunks=(qi.chunks[0],)
                                       , drop_axis=1)
    camera_grid = camera_grid_future.compute()
    camera_grid = camera_grid.reshape((N, N, N))

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
    plt.savefig('volumerender' + str(i) + '_dask.png', dpi=240, bbox_inches='tight', pad_inches=0)

# @delayed
def simple_projection(datacube):
    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection_dask.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()

# @profile
def main():
    """ Volume Rendering """
    # Start Dask Client
    client = Client(n_workers=12)

    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = np.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx / 2, Nx / 2, Nx)
    y = np.linspace(-Ny / 2, Ny / 2, Ny)
    z = np.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Viewing Angles
    Nangles = 10

    for i in range(Nangles):
        render(i, points, datacube, Nangles)
    simple_projection(datacube)
    # # Good to scatter big data to all worker processes
    # big_future_datacube = client.scatter(datacube)
    # # Render
    # tasks = [render(i, points, big_future_datacube, Nangles) for i in range(Nangles)]
    # # Plot Simple Projection -- for Comparison
    # tasks.append(simple_projection(big_future_datacube))
    # # Compute
    # dask.compute(tasks)

    # Close Dask Client
    client.close()
    return 0


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print('Time: ', end - start)