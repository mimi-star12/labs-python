
class Author:
    def __init__(self, name: str, group: str = 'P3122'):
        '''
        функция инициализации (создания) объекта класса
        вызывается 1 раз для 1 объекта
        '''
        self.name = name #вызывает сеттер
        self.group = group
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and len(value)>1:
            self._name = value
        else:
            raise TypeError('некорректное имя: должно быть строкой и содержать >1 символа')

    @property 
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, value: str):
        if isinstance(value, str) and len(value)>4:
            self._group = value
        else:
            raise TypeError('некорректная группа: должна быть строкой и содержать >4 символов')
        
a=Author('mimi')
print(a.name)

a.name='koko'
print(a.name)