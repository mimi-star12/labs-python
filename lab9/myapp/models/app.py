from .author import Author


class App:
    """
    Модель приложения.
    """
    def __init__(self, name: str, version: float, author: Author):
        self.name = name
        self.version = version
        self.author = author 
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and len(value) > 1:
            self._name = value
        else:
            raise TypeError("name должно быть строкой и содержать >1 символа")
    
    @property
    def version(self):
        return self._version 
    @version.setter
    def version(self, value: float):
        if isinstance(value, (float, int)) and value > 0:
            self._version = float(value)
        else:
            raise TypeError("version должен быть числом больше 0")

    @property
    def author(self):
        return self._author
    @author.setter
    def author(self, value: Author):
        if isinstance(value, Author):
            self._author = value
        else:
            raise TypeError("author должен быть объектом класса Author")
        