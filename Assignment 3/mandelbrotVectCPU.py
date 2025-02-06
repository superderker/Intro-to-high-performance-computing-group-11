import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter as time

def mandelbrot(c, max_iter=1000):
    """Computes the number of iterations before divergence."""
    z = np.zeros(c.shape)
    add=np.zeros(c.shape)
    for n in range(max_iter):
        z=np.where(np.abs(z)<2, z * z + c, z)
        add+=np.abs(z)<2
    return add

def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter=1000):
    """Generates the Mandelbrot set image."""
    x_vals = [np.linspace(x_min, x_max, width)]*height
    y_vals = np.atleast_2d(np.linspace(y_min*1j, y_max*1j, height)).T
    image = np.zeros((height, width))
    cT=x_vals+y_vals
    return mandelbrot(cT, max_iter)

# Parameters
width, height = 1000, 800
x_min, x_max, y_min, y_max = -2, 1, -1, 1

# Generate fractal
t1=time()
image = mandelbrot_set(width, height, x_min, x_max, y_min, y_max)
print(time()-t1)
# Display
plt.imshow(image, cmap='inferno', extent=[x_min, x_max, y_min, y_max])
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()