import timeit
import math

import cy_integrate
from nogil_processes import integrate_sin_nogil_processes
from nogil_threads import integrate_sin_nogil_threads
from integrate import integrate
from threads import integrate_threads
from processes import integrate_process


def time_integrate(f):
    time1 = timeit.timeit(lambda: f(math.sin, 0, math.pi, n_iter=10**4), number = 3)
    time2 = timeit.timeit(lambda: f(math.sin, 0, math.pi, n_iter=10**5), number = 3)
    time3 = timeit.timeit(lambda: f(math.sin, 0, math.pi, n_iter=10**6), number = 3)
    return time1, time2, time3

def time_nogil(f):
    time1 = timeit.timeit(lambda: f(0, math.pi, n_iter=10**4), number = 3)
    time2 = timeit.timeit(lambda: f(0, math.pi, n_iter=10**5), number = 3)
    time3 = timeit.timeit(lambda: f(0, math.pi, n_iter=10**6), number = 3)
    return time1, time2, time3

def main():
    print("Базовый способ:", time_integrate(integrate))
    print("Потоки:", time_integrate(integrate_threads))
    print("Процессы:", time_integrate(integrate_process))
    print("Cython:", time_integrate(cy_integrate.integrate_any))
    print("Cython с потоками:", time_nogil(integrate_sin_nogil_threads))
    print("Cython с процессами:", time_nogil(integrate_sin_nogil_processes))

if __name__ == "__main__":
    main()