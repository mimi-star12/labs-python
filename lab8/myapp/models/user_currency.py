
class UserCurrency:
    """
    Связь подписки пользователя на валюту (user_id и currency_id).
    """
    _next_id = 1  # общий счётчик для всех подписок

    def __init__(self, user_id: int, currency_id: str) -> None:
        # авто-id
        self._id = UserCurrency._next_id
        UserCurrency._next_id += 1

        # остальное через setters
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def currency_id(self) -> str:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise TypeError("currency_id должен быть непустой строкой")
        self._currency_id = value

    @property
    def user_id(self) -> int:
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise TypeError("user_id должен быть целым числом больше 0")
        self._user_id = value

    