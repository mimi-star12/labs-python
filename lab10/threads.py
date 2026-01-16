import concurrent.futures as ftres
from typing import Callable

from integrate import integrate

def integrate_threads(f: Callable[[float], float], a: float, b: float, *, threads: int = 2, n_iter: int = 100000) -> float:

    if threads < 1:
        raise ValueError("threads должен быть >= 1")
    if n_iter < 1:
        raise ValueError("n_iter должен быть >= 1")

    iter_per_thread = n_iter // threads
    chunk = (b - a) / threads
    final = 0.0
    results = []

    with ftres.ThreadPoolExecutor(max_workers=threads) as executor:

        for i in range(threads):
            left = a + i * chunk
            right = a + (i + 1) * chunk

            # запускаем обычный integrate на кусочке
            results.append(executor.submit(integrate, f, left, right, n_iter=iter_per_thread))

        # забираем результаты
        for fut in results:
            final += fut.result()

    return final