class User:
    _next_id = 1  # общий счётчик для всех пользователей

    def __init__(self, name: str):
        # авто-id
        self._id = User._next_id
        User._next_id += 1

        # остальное через setter
        self.name = name

    @property
    def id(self) -> int:
        return self._id  # read-only


    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise TypeError('некорректное имя: должно быть строкой и содержать >1 символа')

