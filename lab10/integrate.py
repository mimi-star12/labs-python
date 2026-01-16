import math
import doctest
from typing import Callable


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    """
    Численно вычисляет интеграл функции f(x) на отрезке [a, b] методом прямоугольников.

    Params:
        f: функция от одного аргумента (f(x) -> число)
        a: левая граница
        b: правая граница
        n_iter: число разбиений (чем больше, тем точнее и тем дольше)

    Returns:
        Приближённое значение интеграла (float).
    
    >>> round(integrate(math.sin, 0, math.pi, n_iter=200000), 3)
    2.0
    >>> round(integrate(lambda x: x*x, 0, 1, n_iter=200000), 3)
    0.333
    """
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

doctest.run_docstring_examples(integrate, globals())
# print(integrate(math.cos, 0, math.pi, n_iter=1000) )