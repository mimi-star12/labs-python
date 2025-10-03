
def two_sum(nums,target):
    ans=[]
    if len(nums)<2:
        raise ValueError('not enough arguments given') # добавила эту строку, чтобы юзеру было понятно, почему код не работает
    
    for i in range(len(nums)-1):
        if type(nums[i])==str: # добавила проверку на тип, чтобы код мог работать, даже если юзер по ошибке введет str данные
            pass
        else:
            for k in range(i+1,len(nums)):
                if type(nums[k])==str:
                    pass
                else:
                    if nums[i]+nums[k] == target:
                        ans.append(i)
                        ans.append(k)
                        return(ans)
                    
# снизу проверяла работу кода, оставила для наглядности 

# print(two_sum(['re',3, 'g',4],7))          
# print(two_sum(['re',3,4],7))
# print(two_sum([3,3,3,3],6))
# assert two_sum([3,3,3,3]==[0,1])

