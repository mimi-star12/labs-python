import concurrent.futures as ftres
from typing import Callable

from integrate import integrate

def integrate_process(f: Callable[[float], float], a: float, b: float, *, processes: int = 2, n_iter: int = 100000) -> float:

    if processes < 1:
        raise ValueError("processes должен быть >= 1")
    if n_iter < 1:
        raise ValueError("n_iter должен быть >= 1")

    iter_per_proc = n_iter // processes
    chunk = (b - a) / processes
    final = 0.0
    futures = []

    with ftres.ProcessPoolExecutor(max_workers=processes) as executor:
        for i in range(processes):
            left = a + i * chunk
            right = a + (i + 1) * chunk
            futures.append(executor.submit(integrate, f, left, right, n_iter=iter_per_proc))

        for fut in futures:
            final += fut.result()

    return final
