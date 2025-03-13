import timeit
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

CHUNK_SIZE = 128
INPUT_CHUNK = (CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)
TARGET_SHAPE = (90, 90, 90)
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

def process_block(block, Nangles, i, points, block_info=None):
    block_index = block_info[0]['chunk-location']
    # print("block_index:", block_index)

    # 计算当前块在全局坐标系统中的位置
    x_range = (block_index[0] * CHUNK_SIZE, (block_index[0] + 1) * CHUNK_SIZE)
    y_range = (block_index[1] * CHUNK_SIZE, (block_index[1] + 1) * CHUNK_SIZE)
    z_range = (block_index[2] * CHUNK_SIZE, (block_index[2] + 1) * CHUNK_SIZE)

    # 提取当前块对应的局部 points
    local_points = (points[0][x_range[0]:x_range[1]], points[1][y_range[0]:y_range[1]], points[2][z_range[0]:z_range[1]])

    angle = np.pi / 2 * i / Nangles
    c = np.linspace(-N/2, N/2, N)
    qx, qy, qz = np.meshgrid(c,c,c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle)
    qzR = qy * np.sin(angle) + qz * np.cos(angle)

    qi_size = int(N / (256 / CHUNK_SIZE))
    qxR = qxR[block_index[0] * qi_size: (block_index[0] + 1) * qi_size,
          block_index[0] * qi_size: (block_index[0] + 1) * qi_size,
          block_index[0] * qi_size: (block_index[0] + 1) * qi_size]
    qyR = qyR[block_index[1] * qi_size: (block_index[1] + 1) * qi_size,
            block_index[1] * qi_size: (block_index[1] + 1) * qi_size,
            block_index[1] * qi_size: (block_index[1] + 1) * qi_size]
    qzR = qzR[block_index[2] * qi_size: (block_index[2] + 1) * qi_size,
            block_index[2] * qi_size: (block_index[2] + 1) * qi_size,
            block_index[2] * qi_size: (block_index[2] + 1) * qi_size]

    qi_sub = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T

    interp_values = interpn(local_points, block, qi_sub, method='linear').reshape(TARGET_SHAPE)
    # interp_values = interpn(local_points, block, qi_sub, method='linear')

    print(f"interp_values:", interp_values.shape, "block_index:", block_index, "\n")

    return interp_values


def render_single_angle(i, datacube_dask, Nangles, points):
    # 使用map_blocks分块计算
    da_grid = da.map_blocks(
        process_block,
        datacube_dask, Nangles=Nangles, i=i, points=points,
        dtype=np.float32,
        chunks=TARGET_SHAPE,
        block_info=True
    )
    temp_grid = da_grid.compute()
    #
    # blocks = []
    # for i in range(2):
    #     for j in range(2):
    #         for k in range(2):
    #             # 计算每个块的起始和结束索引
    #             x_start = i * temp_grid.shape[0] / 2
    #             x_end = (i + 1) * temp_grid.shape[0] / 2
    #             y_start = j * temp_grid.shape[1] / 2
    #             y_end = (j + 1) * temp_grid.shape[1] / 2
    #             z_start = k * temp_grid.shape[2] / 2
    #             z_end = (k + 1) * temp_grid.shape[2] / 2
    #
    #             # print(f"x_start: {x_start}, x_end: {x_end}, y_start: {y_start}, y_end: {y_end}, z_start: {z_start}, z_end: {z_end}")
    #
    #             block = temp_grid[int(x_start):int(x_end), int(y_start):int(y_end), int(z_start):int(z_end)]
    #             # block = temp_grid[i * 729000:(i + 1) * 729000, j:(j + 1), k:(k + 1)]
    #
    #             print(f"Block ({i}, {j}, {k}) shape: {block.shape}")
    #
    #             # 将展平后的块添加到列表中
    #             blocks.append(block)
    # print("blocks.shape:", len(blocks))
    # camera_grid = np.concatenate([block.ravel() for block in blocks]).reshape(180, 180, 180)

    # camera_grid = da.concatenate(da_grid, axis=0)
    # camera_grid.compute()
    # print(f"camera_grid shape:", camera_grid.shape)
    # camera_grid.reshape(TARGET_SHAPE)
    # print("Final array shape:", camera_grid.shape)

    # Do Volume Rendering
    # image.shape=(180, 180, 3)
    camera_grid = temp_grid
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

@delayed
def simple_projection(datacube):
    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection_dask.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()

def main():
    """ Volume Rendering """

    # Start Dask Client
    client = Client(n_workers=4)

    # Load Datacube
    with h5.File('datacube.hdf5', 'r') as f:
        # 将数据完全加载到内存中，避免后续依赖HDF5文件
        data_numpy = np.array(f['density'])
        datacube = da.from_array(data_numpy, chunks=INPUT_CHUNK)

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx / 2, Nx / 2, Nx)
    y = np.linspace(-Ny / 2, Ny / 2, Ny)
    z = np.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Viewing Angles
    Nangles = 10
    for i in range(Nangles):
        print(f'Rendering Scene {i+1} of {Nangles}')
        start1 = timeit.default_timer()
        render_single_angle(i, datacube, Nangles, points)
        end1 = timeit.default_timer()
        print(f'Time: , {i+1} = [{end1 - start1}]')
    # simple_projection(datacube)

    # Plot Volume Rendering
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection_dask.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()

    # Close Dask Client
    client.close()
    return 0

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print('Time: ', end - start)