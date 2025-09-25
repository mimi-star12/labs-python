
def guess(n: int,lst: list) -> (int, int):
    '''binary search function'''
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
'''вовзращает искомое число и кол-во входов'''



def main() -> 'function':
    print('what do we search?')
    num=int(input())
    
    print('input start of the list')
    n=int(input())
    
    print('input end of the list')
    f=int(input())
    
    '''filling in list'''
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


# print (main())
'''проверить работу вручную'''
