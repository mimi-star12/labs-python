import concurrent.futures as ft
import cy_nogil

def integrate_sin_nogil_processes(a, b, *, processes=2, n_iter=1_000_000):
    chunk = (b - a) / processes
    iter_per = n_iter // processes

    total = 0.0
    with ft.ProcessPoolExecutor(max_workers=processes) as ex:
        futures = []
        for i in range(processes):
            left = a + i * chunk
            right = a + (i + 1) * chunk
            futures.append(ex.submit(cy_nogil.integrate_sin_nogil, left, right, iter_per))

        for f in futures:
            total += f.result()

    return total