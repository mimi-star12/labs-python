# cy_nogil.pyx
# cython: language_level=3

cimport cython
from libc.math cimport sin

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double integrate_sin_nogil(double a, double b, int n_iter=100000) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x

    if n_iter <= 0:
        return 0.0

    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step

    return acc
