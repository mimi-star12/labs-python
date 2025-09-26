
def guess(n: int, lst: list) -> (int, int):
    '''Функция бинарного поиска искомого числа в списке.

    Ищет число 'n' в отсортированном списке 'lst' с помощью
    алгоритма бинарного поиска.

    Аргументы:
        n (int) -- искомое число.
        lst (list) -- отсортированный список, в котором производится поиск.

    Возвращает: 
        кортеж, содержащий найденное число (lst[right])
        и количество итераций (k), потребовавшихся для поиска.

    Raises:
        ValueError: если искомое число не найдено в списке.
    '''
    if n not in lst:
        raise ValueError('искомое число не в списке')
        
    left=-1
    right=len(lst)
    k=1 
    while left<right-1: #works until only 2 numbers left
        mid=(left+right)//2
        k+=1
        if lst[mid]>=n:
            right=mid
        else:
            left=mid
    return lst[right],k




def main() -> 'function':
    '''Создает список 'lst' в котором будет производиться поиск числа 'n' на основе данных, 
    которые вводит пользователь:

    num -- int (искомое число)
    n -- int (начало списка)
    f -- int (конец списка)

    Формирует список значений в интервале от n до f (если возможно) 

    ValueError: если не удалось сформировать список (пользователь
    отказался поменять местами n и f).

    Вызывает функцию guess (бинарный поиск)
    '''
    print('what do we search?')
    num=int(input())
    
    print('input start of the list')
    n=int(input())
    
    print('input end of the list')
    f=int(input())
    
    if n<f:
        lst=[int(x) for x in range(n,f+1)] 
    else:
        print('impossible to form a list. swap n and f?? (YES/NO)')
        g=input('')
        if (g=='yes' or g=='Yes' or g=='YES'):
            lst=[int(x) for x in range(f,n+1)]
        else:
            raise ValueError('impossible list')
    return(guess(num,lst))

# print(guess.__doc__)
# print(main.__doc__)

# print (main())

