import concurrent.futures as ft
import cy_nogil

def integrate_sin_nogil_threads(a, b, *, threads=2, n_iter=1_000_000):
    chunk = (b - a) / threads
    iter_per = n_iter // threads

    total = 0.0
    with ft.ThreadPoolExecutor(max_workers=threads) as ex:
        futures = []
        for i in range(threads):
            left = a + i * chunk
            right = a + (i + 1) * chunk
            futures.append(ex.submit(cy_nogil.integrate_sin_nogil, left, right, iter_per))

        for f in futures:
            total += f.result()

    return total