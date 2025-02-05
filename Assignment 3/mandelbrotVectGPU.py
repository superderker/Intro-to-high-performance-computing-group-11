import numpy as np
import torch as tc
import matplotlib.pyplot as plt
from time import perf_counter as time

def mandelbrot(c, max_iter=1000):
    """Computes the number of iterations before divergence."""
    z = tc.zeros(c.shape).cuda()
    add=tc.zeros(c.shape).cuda()
    for n in range(max_iter):
        z=tc.where(tc.abs(z)<2, z * z + c, z)
        add+=tc.abs(z)<2
    return add

def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter=1000):
    """Generates the Mandelbrot set image."""
    x_vals =tc.Tensor(tc.linspace(x_min, x_max, width))
    y_vals =tc.transpose(tc.atleast_2d(tc.linspace(y_min*1j, y_max*1j, height)),0,1)
    cT=tc.add(x_vals.unsqueeze(0).repeat(height,1), y_vals).cuda()
    return mandelbrot(cT, max_iter)

# Parameters
width, height = 1000, 800
x_min, x_max, y_min, y_max = -2, 1, -1, 1

# Generate fractal
t1=time()
image = mandelbrot_set(width, height, x_min, x_max, y_min, y_max)
print(time()-t1)
# Display
plt.imshow(tc.Tensor.cpu(image), cmap='inferno', extent=[x_min, x_max, y_min, y_max])
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()