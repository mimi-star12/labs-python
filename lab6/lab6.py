import timeit
import matplotlib.pyplot as plt

from lab3 import lab3
from lab5 import lab5

def benchmark(func, root, number=10000, repeat=5):
    """Возвращает среднее время выполнения func на корне root"""
    times = timeit.repeat(lambda: func(root, 8), number=number, repeat=repeat)
    # берём минимальное время из серии
    return (min(times)/number)

t1, t2 = [], []
for i in range(10):
    t1.append(benchmark(lab3.get_bin_tree, i))
    t2.append(benchmark(lab5.get_bin_tree_iter, i))
# строим график
y = range(10)
plt.plot(y, t1, label='Рекурсивный')
plt.plot(y, t2, label='Итеративный')
plt.xlabel("Высота дерева")
plt.ylabel("Время")
plt.title("Сравнение рекурсивного и итеративного построения дерева")
plt.legend()
plt.show()

# Вывод ---> рекурсивный подход работает быстрее на небольших высотах дерева, 
# но при увеличении высоты итеративный подход становится предпочтительнее