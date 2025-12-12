import functools
import requests
import sys
import logging
import io

file_logger = logging.getLogger("currency")
file_logger.setLevel(logging.INFO)

handler = logging.FileHandler("currency.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
handler.setFormatter(formatter)

file_logger.addHandler(handler)
file_logger.propagate = False

def logger(func=None, *, handle=sys.stdout):
    '''
    Декоратор для логирования вызовов функции в указанный обработчик (файл или консоль)

    Args:
        func: функция для декорирования (по умолчанию None)
        handle (file-like object or logging.Logger): обработчик для логирования (по умолчанию sys.stdout)
    Returns:
        Декорированная функция с логированием
    '''
    if func is None:
        return lambda real_func: logger(real_func, handle=handle)
    else:
        @functools.wraps(func)
        def wrapper (*args, **kwargs):
            '''
            Внутренняя обертка для логирования вызовов функции

            Args:
                *args: позиционные аргументы функции
                **kwargs: именованные аргументы функции
            '''
            if isinstance(handle, logging.Logger):
                try:
                    handle.info(f"starting func {func.__name__} with args {args} {kwargs}")
                    result = func(*args, **kwargs)
                    handle.info(f"successfully finished! result {result}")
                    return result
                except Exception as e:
                    handle.error(f"ERROR: {type(e).__name__} {e}", exc_info=True)
                    raise

            else:
                try:
                    handle.write(f"starting func {func.__name__} with args {args} {kwargs}\n")
                    result = func(*args, **kwargs)
                    handle.write(f"successfully finished! result {result}\n")
                    return result
                except Exception as e:
                    handle.write(f"ERROR: {type(e).__name__} {e}\n")
                    raise
    
    return wrapper


url = 'https://www.cbr-xml-daily.ru/daily_json.js'

@logger(handle = file_logger)
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

if __name__ == "__main__":
    currencies = ["USD", "EUR", "NGN", "CNY"]
    print(get_currencies(currencies))


                

    



