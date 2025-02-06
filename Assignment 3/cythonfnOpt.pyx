cimport cython
import numpy as np
cimport numpy as np
#cythonfnOpt.pyx
@cython.boundscheck(False)
def gauss_seidel(double[:, :] f):
    cdef double[:, :] newf
    cdef unsigned int i, j
    newf = np.copy(f)
    for i in range(1,newf.shape[0]-1):
        for j in range(1,newf.shape[1]-1):
            newf[i][j] = 0.25 * (newf[i][j+1] + newf[i][j-1] +
                                   newf[i+1][j] + newf[i-1][j])
    
    return newf