import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import time

"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""
times = {}
def transferFunction(x):
	
	r = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
	g = 1.0*np.exp( -(x - 9.0)**2/1.0 ) +  1.0*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
	b = 0.1*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  1.0*np.exp( -(x - -3.0)**2/0.5 )
	a = 0.6*np.exp( -(x - 9.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) + 0.01*np.exp( -(x - -3.0)**2/0.5 )
	
	return r,g,b,a


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

def interpol(i, points, datacube, Nangles):
    angle = np.pi/2 * i / Nangles
    N = 180
    c = np.linspace(-N/2, N/2, N)
    qx, qy, qz = np.meshgrid(c,c,c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle) 
    qzR = qy * np.sin(angle) + qz * np.cos(angle)
    qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    # Interpolate onto Camera Grid
    camera_grid = interpn(points, datacube, qi, method='linear').reshape((N,N,N))
    
    # Do Volume Rendering
    image = np.zeros((camera_grid.shape[1],camera_grid.shape[2],3))
    return image ,camera_grid

def color_transfer(image, dataslice):
    r,g,b,a = transferFunction(np.log(dataslice))
    image[:,:,0] = a*r + (1-a)*image[:,:,0]
    image[:,:,1] = a*g + (1-a)*image[:,:,1]
    image[:,:,2] = a*b + (1-a)*image[:,:,2]
    return image
def plot_image(image, i):
    plt.figure(figsize=(4,4), dpi=80)
    
    plt.imshow(image)
    plt.axis('off')
    
    # Save figure
    plt.savefig('volumerender' + str(i) + '.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
    
def plot_projection(datacube):
    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4,4), dpi=80)
    
    plt.imshow(np.log(np.mean(datacube,0)), cmap = 'viridis')
    plt.clim(-5, 5)
    plt.axis('off')
    
    # Save figure
    plt.savefig('projection.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
    plt.show()
def main():
    """ Volume Rendering """
    # Load Datacube
    t1 = time.perf_counter()
    datacube = load_data()
    t2 = time.perf_counter()
    tFinal = t2 - t1
    print(f"Loading data took {tFinal:.6f} seconds")
    times["load_data"] = tFinal
    # Datacube Grid
    # Do Volume Rendering at Different Viewing Angles
    t1 = time.perf_counter()
    points = get_data_points(datacube)
    t2 = time.perf_counter()
    tFinal = t2 - t1
    times ["get_data_points"] = tFinal
    print(f" getting data points took: {tFinal:.6f} seconds")
    Nangles = 10
    outer_loop_times = []
    inner_loop_times = []
    t5 = time.perf_counter()
    for i in range(Nangles):
        t3 = time.perf_counter()
        t1 = time.perf_counter()
        image, camera_grid = interpol(i, points, datacube, Nangles)
        t2 = time.perf_counter()
        tFinal = t2 - t1
        # print(f"Interpoling took: {tFinal:.6f} seconds")
        loop_times = []
        
        
        # this part can be vectorized so that operations are done on the whole array at once
        for dataslice in camera_grid:
            t1 = time.perf_counter()
            image = np.clip(image,0.0,1.0)
            image = color_transfer(image, dataslice)
            t2 = time.perf_counter()
            tFinal = t2 - t1
            loop_times.append(tFinal)
            # print(f"Color transfer took: {tFinal:.6f} seconds")
        t4 = time.perf_counter()
        tFinal = t4 - t3
        outer_loop_times.append(tFinal)
        # Plot Volume Rendering
        mean_loop_time = np.mean(loop_times)
        inner_loop_times.append(loop_times)
        
        # print(f"Mean loop time: {mean_loop_time:.6f} seconds")
        plot_image(image, i)
    t6 = time.perf_counter()
    mean_outer_loop_time = np.mean(outer_loop_times)
    times["mean_outer_loop_time"] = mean_outer_loop_time
    print(f"Mean outer loop time: {mean_outer_loop_time:.6f} seconds")
    total_time = t6 - t5
    print(f"Total time for loop: {total_time:.6f} seconds")
    plot_projection(datacube)
    plot_outer_loop_times(outer_loop_times)
    plot_inner_loop_times_mean(inner_loop_times)
    plot_inner_loop_times_std(inner_loop_times)
    print_times()
    return 0
	
def plot_outer_loop_times(outer_loop_times):
    print("longest loop was: ", max(outer_loop_times))
    plt.figure(figsize=(8, 4), dpi=80)
    plt.plot(outer_loop_times, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteration')
    plt.ylabel('Time (seconds)')
    plt.title('Outer Loop Times')
    plt.grid(True)
    plt.savefig('outer_loop_times.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()
    
	
def plot_inner_loop_times_mean(inner_loop_times):
    inner_loop_times_mean = []
    for i in range(len(inner_loop_times)):
        inner_loop_times_mean.append(np.mean(inner_loop_times[i]))
    plt.figure(figsize=(8, 4), dpi=80)
    plt.plot(inner_loop_times_mean, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteration')
    plt.ylabel('Time (seconds)')
    plt.title('Inner Loop Times mean')
    plt.grid(True)
    plt.savefig('Inner_loop_times.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()
def plot_inner_loop_times_std(inner_loop_times):
    inner_loop_times_std = []
    for i in range(len(inner_loop_times)):
        inner_loop_times_std.append(np.std(inner_loop_times[i]))
    plt.figure(figsize=(8, 4), dpi=80)
    plt.plot(inner_loop_times_std, marker='o', linestyle='-', color='y')
    plt.xlabel('Iteration')
    plt.ylabel('Time (seconds)')
    plt.title('Inner Loop Times std')
    plt.grid(True)
    plt.savefig('Inner_loop_times_std.png', dpi=240, bbox_inches='tight', pad_inches=0)
    plt.show()
  
def print_times():
    for key, value in times.items():
        print(f"{key} took {value:.6f} seconds to execute.")
if __name__== "__main__":
  main()


