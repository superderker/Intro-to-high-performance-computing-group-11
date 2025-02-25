# import numpy as np
# import matplotlib.pyplot as plt
# import h5py as h5
# from scipy.interpolate import interpn
# import time
# import line_profiler

# """
# Create Your Own Volume Rendering (With Python)
# Philip Mocz (2020) Princeton Univeristy, @PMocz

# Simulate the Schrodinger-Poisson system with the Spectral method
# """
# times = {}

# @profile
# def transferFunction(x):
	
# 	r = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
# 	g = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  1.0*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
# 	b = 0.1*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  1.0*np.exp( -(x - -3.0)**2/0.5 )
# 	a = 0.6*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) + 0.01*np.exp( -(x - -3.0)**2/0.5 )
	
# 	return r,g,b,a


# def load_data():
#     f = h5.File('datacube.hdf5', 'r')
#     datacube = np.array(f['density'])
#     return datacube
# def get_data_points(datacube):
#     Nx, Ny, Nz = datacube.shape
#     x = np.linspace(-Nx/2, Nx/2, Nx)
#     y = np.linspace(-Ny/2, Ny/2, Ny)
#     z = np.linspace(-Nz/2, Nz/2, Nz)
#     points = (x, y, z)
#     return points

# @profile
# def interpol(i, points, datacube, Nangles):
#     angle = np.pi/2 * i / Nangles
#     N = 180
#     c = np.linspace(-N/2, N/2, N)
#     qx, qy, qz = np.meshgrid(c,c,c)
#     qxR = qx
#     qyR = qy * np.cos(angle) - qz * np.sin(angle) 
#     qzR = qy * np.sin(angle) + qz * np.cos(angle)
#     qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
#     # Interpolate onto Camera Grid
#     camera_grid = interpn(points, datacube, qi, method='linear').reshape((N,N,N))
    
#     # Do Volume Rendering
#     image = np.zeros((camera_grid.shape[1],camera_grid.shape[2],3))
#     return image ,camera_grid

# @profile
# def color_transfer(image, dataslice):
#     r,g,b,a = transferFunction(np.log(dataslice))
#     image[:,:,0] = a*r + (1-a)*image[:,:,0]
#     image[:,:,1] = a*g + (1-a)*image[:,:,1]
#     image[:,:,2] = a*b + (1-a)*image[:,:,2]
#     return image
# def plot_image(image, i):
#     plt.figure(figsize=(4,4), dpi=80)
    
#     plt.imshow(image)
#     plt.axis('off')
    
#     # Save figure
#     plt.savefig('volumerender' + str(i) + '.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
    
# def plot_projection(datacube):
#     # Plot Simple Projection -- for Comparison
#     plt.figure(figsize=(4,4), dpi=80)
    
#     plt.imshow(np.log(np.mean(datacube,0)), cmap = 'viridis')
#     plt.clim(-5, 5)
#     plt.axis('off')
    
#     # Save figure
#     plt.savefig('projection.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
#     plt.show()
# def main():
#     """ Volume Rendering """
#     # Load Datacube
#     datacube = load_data()
#     points = get_data_points(datacube)
#     Nangles = 10
#     for i in range(Nangles):
#         image, camera_grid = interpol(i, points, datacube, Nangles)
        
        
#         # this part can be vectorized so that operations are done on the whole array at once
#         for dataslice in camera_grid:
#             image = np.clip(image,0.0,1.0)
#             image = color_transfer(image, dataslice)
#         # Plot Volume Rendering
#         plot_image(image, i)
#     plot_projection(datacube)
#     return 0

  
# if __name__== "__main__":
#   main()


import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import time
from memory_profiler import profile

"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton University, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""

times = {}

@profile
def transferFunction(x):
    r = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
    g = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  1.0*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
    b = 0.1*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  1.0*np.exp( -(x - -3.0)**2/0.5 )
    a = 0.6*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) + 0.01*np.exp( -(x - -3.0)**2/0.5 )
    return r, g, b, a


def load_data():
    f = h5.File('datacube.hdf5', 'r')
    datacube = np.array(f['density'])
    return datacube


def get_data_points(datacube):
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx/2, Nx/2, Nx)
    y = np.linspace(-Ny/2, Ny/2, Ny)
    z = np.linspace(-Nz/2, Nz/2, Nz)
    points = (x, y, z)
    return points

@profile
def interpol(i, points, datacube, Nangles):
    angle = np.pi/2 * i / Nangles
    N = 180
    c = np.linspace(-N/2, N/2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle) 
    qzR = qy * np.sin(angle) + qz * np.cos(angle)
    qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    
    # Interpolate onto Camera Grid
    camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
    
    # Do Volume Rendering
    image = np.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))
    return image, camera_grid

@profile
def color_transfer(image, dataslice):
    r, g, b, a = transferFunction(np.log(dataslice))
    image[:, :, 0] = a * r + (1 - a) * image[:, :, 0]
    image[:, :, 1] = a * g + (1 - a) * image[:, :, 1]
    image[:, :, 2] = a * b + (1 - a) * image[:, :, 2]
    return image


def plot_image(image, i):
    plt.figure(figsize=(4, 4), dpi=80)
    plt.imshow(image)
    plt.axis('off')
    plt.savefig(f'volumerender{i}.png', dpi=240, bbox_inches='tight', pad_inches=0)


def plot_projection(datacube):
    plt.figure(figsize=(4, 4), dpi=80)
    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()

@profile
def main():
    """ Volume Rendering """
    datacube = load_data()
    points = get_data_points(datacube)
    Nangles = 10
    for i in range(Nangles):
        image, camera_grid = interpol(i, points, datacube, Nangles)
        for dataslice in camera_grid:
            image = np.clip(image, 0.0, 1.0)
            image = color_transfer(image, dataslice)
        plot_image(image, i)
    plot_projection(datacube)
    return 0

if __name__ == "__main__":
    main()