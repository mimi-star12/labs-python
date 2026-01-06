class Currency:
    '''
    id — уникальный идентификатор

    num_code — цифровой код

    char_code — символьный код

    name — название валюты

    value — курс

    nominal — номинал (за сколько единиц валюты указан курс)
    '''
    def __init__(
            self, 
            id: str,
            num_code: int, 
            char_code: str, 
            name:str, 
            value: float|int, 
            nominal: int
        ):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: str):
        if isinstance(value, str) and value.strip():
            self._id = value
        else:
            raise TypeError("ID должен быть не пустой строкой")

    @property
    def num_code(self):
        return self._num_code

    @num_code.setter
    def num_code(self, value: int):
        if isinstance(value, int) and value > 0:
            self._num_code = value
        else:
            raise TypeError("Num_code должен быть числом больше 0")

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, value: str):
        if isinstance(value, str) and value.strip():
            self._char_code = value
        else:
            raise TypeError("Char_code должен быть не пустой строкой")

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise TypeError("Name должен быть не пустой строкой")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float|int):
        if isinstance(value, (float, int)) and value > 0:
            self._value = value
        else:
            raise TypeError("Value должен быть числом больше 0")
    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value: int):
        if isinstance(value, int) and value > 0:
            self._nominal = value
        else:
            raise TypeError("Nominal должен быть числом больше 0 ")