
class UserCurrency:
    """
    Связь подписки пользователя на валюту (user_id и currency_id).
    """

    def __init__(self, user_id: int, currency_id: str):
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        self._user_id = value

    @property
    def currency_id(self) -> str:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("currency_id должен быть непустой строкой")
        self._currency_id = value