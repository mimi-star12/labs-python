class User:
    def __init__(self, id: int, name: str):
        self._id = id
        self.name = name

    @property
    def id(self) -> int:
        return self._id
    

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 1:
            self._name = value
        else:
            raise TypeError('некорректное имя: должно быть строкой и содержать >1 символа')

