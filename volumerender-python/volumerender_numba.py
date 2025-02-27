import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import timeit
from memory_profiler import profile
from numba import jit, njit, vectorize, float64, guvectorize

"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""

# @guvectorize(['(float64[:,:], float64[:,:], float64[:,:], float64[:,:], float64[:,:])'], '(n,n)->(n,n), (n,n), (n,n), (n,n)',
#               target='parallel', fastmath=True)
# def transferFunction(x, r, g, b, a):
#     exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
#     exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
#     exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)
#
#     r[:, :] = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
#     g[:, :] = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
#     b[:, :] = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
#     a[:, :] = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3
# using @njit here is not efficient
# # @njit(fastmath=True)
def transferFunction(x):
    exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a

"""
parallel is faster
"""

@vectorize(['float64(float64, float64, float64, float64)'], fastmath=True, target='parallel')
def rotate_qy(qy, qz, cos_angle, sin_angle):
    qyR = qy * cos_angle - qz * sin_angle
    return qyR

@vectorize(['float64(float64, float64, float64, float64)'], fastmath=True, target='parallel')
def rotate_qz(qy, qz, cos_angle, sin_angle):
    qzR = qy * sin_angle + qz * cos_angle
    return qzR


@profile
def main():
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

    # Do Volume Rendering at Different Veiwing Angles
    Nangles = 10
    angle_unit = np.pi / 2 / Nangles
    N = 180
    c = np.linspace(-N / 2, N / 2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    cos_angles = np.cos(angle_unit * np.arange(Nangles))
    sin_angles = np.sin(angle_unit * np.arange(Nangles))

    for i in range(Nangles):
        print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')

        # Camera Grid / Query Points -- rotate camera view
        cos_angle = cos_angles[i]
        sin_angle = sin_angles[i]
        # qxR = qx
        # qyR = qy * cos_angle - qz * sin_angle
        # qzR = qy * sin_angle + qz * cos_angle
        qyR = rotate_qy(qy, qz, cos_angle, sin_angle)
        qzR = rotate_qz(qy, qz, cos_angle, sin_angle)
        # qyR, qzR = rotate(qy, qz, cos_angle, sin_angle)

        # Interpolate onto Camera Grid
        camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
                                         method='linear')).reshape((N, N, N))

        # Do Volume Rendering
        r_channel = np.zeros((N, N))
        g_channel = np.zeros((N, N))
        b_channel = np.zeros((N, N))
        for dataslice_log in camera_grid_log:
            r, g, b, a = transferFunction(dataslice_log)
            r_channel = a * r + (1 - a) * r_channel
            g_channel = a * g + (1 - a) * g_channel
            b_channel = a * b + (1 - a) * b_channel

        image = np.stack((r_channel, g_channel, b_channel), axis=-1)
        image = np.clip(image, 0.0, 1.0)

        # Plot Volume Rendering
        plt.figure(figsize=(4, 4), dpi=80)

        plt.imshow(image)
        plt.axis('off')

        # Save figure
        plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)

    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()

    return 0


if __name__ == "__main__":
    main()
