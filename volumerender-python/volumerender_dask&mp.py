import multiprocessing
import timeit
from multiprocessing import shared_memory

import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from dask.array import block
from dask.array.overlap import boundaries
from scipy.interpolate import interpn
import dask
import dask.array as da
from dask.diagnostics import ProgressBar
from dask import delayed
from dask.distributed import Client

INPUT_CHUNK = (128, 128, 128)   # 输入数据分块大小
OUTPUT_CHUNK = (90, 90, 90)     # 输出数据分块大小
TARGET_SHAPE = (180, 180, 180)  # 最终输出形状
SHARED_MEM_NAME = "datacube_shared"
N = 180

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
    # print("interpolate_block", qi.shape)
    return interpn(points, datacube, qi, method='linear')

def render_single_angle(i, points, shape, dtype, shared_mem_name, Nangles):

    print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    start = timeit.default_timer()

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

    # 将查询点分块
    qi = da.from_array(qi, chunks=(10000, 3))

    # 对每个块并行调用插值函数
    camera_grid_dask = da.map_blocks(
        interpolate_block,
        datacube, points, qi,
        dtype='float32',
        chunks=(qi.chunks[0],),
        drop_axis=1).compute()

    # 将结果转换为三维数组
    camera_grid = camera_grid_dask.reshape((N, N, N))

    # Do Volume Rendering
    image = np.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))

    # 180
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
    end = timeit.default_timer()
    print(f'Time:  {str(i + 1)} [{end - start}]')
    existing_shm.close()

def simple_projection(shape, dtype, shared_mem_name):
    # Plot Simple Projection -- for Comparison
    existing_shm = shared_memory.SharedMemory(name=shared_mem_name)
    datacube = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)

    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()

    existing_shm.close()

def main():
    """ Volume Rendering """

    # Start Dask Client
    client = Client(n_workers=8)

    # Load Datacube
    with h5.File('datacube.hdf5', 'r') as f:
        # 将数据完全加载到内存中，避免后续依赖HDF5文件
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

    # Do Volume Rendering at Different Viewing Angles
    Nangles = 10
    num_process = 10

    with multiprocessing.Pool(processes=num_process) as pool:
        pool.starmap(render_single_angle, [(i, points, datacube.shape, datacube.dtype, SHARED_MEM_NAME, Nangles) for i in range(Nangles)])
        pool.apply(simple_projection, args=(datacube.shape, datacube.dtype, SHARED_MEM_NAME))
        pool.close()
        pool.join()

    shm.close()
    shm.unlink()
    client.close()
    return 0

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print('TotalTime: ', end - start)