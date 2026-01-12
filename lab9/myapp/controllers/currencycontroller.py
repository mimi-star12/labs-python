from controllers.databasecontroller import CurrencyRatesCRUD
from models.currency import Currency
from utils.currencies_api import get_currencies

class CurrencyController:
    def __init__(self, db: CurrencyRatesCRUD):
        self.db = db
    
    def list_currencies(self):
        rows = self.db.read_currencies()  # список кортежей 
        result = []
        for row in rows:
            currency_dict = {
                "id": row[0],
                "num_code": row[1],
                "char_code": row[2],
                "name": row[3],
                "value": row[4],
                "nominal": row[5],
            }
            result.append(currency_dict)
        return result
    
    def delete_currency(self, currency_id: int):
        self.db.delete(currency_id)

    def update_currency(self, char_code: str) -> None:
        '''
        Обновляет валюту через API
        '''
        code = char_code.upper()

        rates = get_currencies([code])
        if code not in rates:
            raise ValueError(f"Курс для {code} не найден в API")

        value = rates[code]
        self.db.update_by_char(code, value)

    def create_currency(self, num_code: str, char_code: str,
                        name: str, value: float, nominal: int):
        currency = Currency(
            num_code=num_code,
            char_code=char_code,
            name=name,
            value=value,
            nominal=nominal,
        )
        self.db.create(
            currency.num_code,
            currency.char_code,
            currency.name,
            currency.value,
            currency.nominal
        )
    
    



