import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter as time
import cythonMandelbrot

# Parameters
width, height = 1000, 800
x_min, x_max, y_min, y_max = -2, 1, -1, 1

# Generate fractal
t1=time()
image = cythonMandelbrot.mandelbrot_set(width, height, x_min, x_max, y_min, y_max)
print(time()-t1)
# Display
plt.imshow(image, cmap='inferno', extent=[x_min, x_max, y_min, y_max])
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()