import requests

url = 'https://www.cbr-xml-daily.ru/daily_json.js'

def get_currencies(currencies_list: list, url: str = url, ) -> dict:
    '''
    Функция получает текущие курсы валют с заданного API (ЦБ РФ) и возвращает dict с курсами указанных валют

    Args:
        currencies_list (list): список валют (строковые коды), курсы которых необходимо получить
        url (str): URL API для получения курсов валют
    Returns:
        dict: словарь с курсами указанных валют
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"API is unavailable at {url}: {e}")
    
    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON {e}") from e
    
    if "Valute" not in data:
        raise KeyError("No 'Valute' in the response JSON")

    valute = data["Valute"]
    result = {}

    for code in currencies_list:
        if code not in valute:
            raise KeyError(f"Currency {code!r} is missing in API response")
        elif not isinstance(valute[code]["Value"], (int, float)):
            raise TypeError(f"Invalid value type for currency {code!r}: expected \
                             int or float, got {type(valute[code]['Value']).__name__}")
        else:
            result[code] = valute[code]["Value"]

    return result