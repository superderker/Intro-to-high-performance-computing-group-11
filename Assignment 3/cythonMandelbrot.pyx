import numpy as np
cimport numpy as np

def mandelbrot(double complex c, int max_iter=1000):
    """Computes the number of iterations before divergence."""
    cdef unsigned int n
    cdef double complex z
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

#mandelbrot_set
def mandelbrot_set(width, height, x_min, x_max, y_min, y_max, max_iter=1000):
    """Generates the Mandelbrot set image."""
    cdef unsigned int i, j
    cdef double complex c
    cdef double[:] x_vals = np.linspace(x_min, x_max, width)
    cdef double[:] y_vals = np.linspace(y_min, y_max, height)
    cdef double[:, :] image = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            c = complex(x_vals[j], y_vals[i])
            image[i][j] = mandelbrot(c, max_iter) #mandelbrot(c, max_iter)

    return image