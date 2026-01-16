# cy_integrate.pyx
# cython: language_level=3

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def integrate_any(f, double a, double b, int n_iter=100000):
    cdef double acc = 0.0
    cdef double step
    cdef int i
    cdef double x

    if n_iter <= 0:
        raise ValueError("n_iter должен быть >= 1")

    step = (b - a) / n_iter

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step   # f(x) — Python вызов (это узкое место)

    return acc