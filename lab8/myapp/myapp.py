import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, User, Currency, UserCurrency, App
from utils.currencies_api import get_currencies


env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape())

true_author = Author('Милана Карелина')
app = App('CurrenciesListApp', 0.2, true_author)
user_1 = User('Chingiz Daddy')
user_2 = User('pipi pupu')
user_3 = User('Ploni Almoni')

allusers = [user_1, user_2, user_3]

user_currencies = [
    UserCurrency(user_1.id, currency_id="USD"),
    UserCurrency(user_2.id, currency_id="EUR"),
    UserCurrency(user_3.id, currency_id="CNY"),
    UserCurrency(user_3.id, currency_id="JPY"),
    UserCurrency(user_3.id, currency_id="GBP"),
]

allcodes = [uc.currency_id for uc in user_currencies]

def build_currency_models(codes):
    """
    Создаёт объекты Currency на основе курсов, полученных из get_currencies.
    """
    rates = get_currencies(codes)
    currencies = []
    for code in codes:
        value = rates.get(code)
        if value is None:
            continue
        currency = Currency(
            id=code, 
            num_code=1,
            char_code=code,
            name=code,
            value=value,
            nominal=1,
        )
        currencies.append(currency)
    return currencies

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            self.handle_index()
        elif path == "/users":
            self.handle_users()
        elif path == "/user":
            self.handle_user(query)
        elif path == "/currencies":
            self.handle_currencies()
        elif path == "/author":
            self.handle_author()
        elif path.startswith("/static/"): 
            self.handle_static(path) 
        else:
            self.send_error(404, "Not Found")

    def handle_static(self, path: str):
        """
        Отдаёт файлы из каталога static (CSS, JS, изображения).
        """
        # Получаем абсолютный путь к файлу на основе пути запроса
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, path.lstrip("/"))

        # Проверяем существует ли файл
        if not os.path.isfile(file_path):
            self.send_error(404, "Static file not found")
            return

        # Определяем тип содержимого в зависимости от расширения
        if file_path.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        elif file_path.endswith(".js"):
            content_type = "application/javascript; charset=utf-8"
        elif file_path.endswith(".ico"):
            content_type = "image/x-icon"
        elif file_path.endswith(".png"):
            content_type = "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        else:
            content_type = "application/octet-stream"

        # Открываем файл и отправляем его содержимое в ответ
        with open(file_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    
    def render_template(self, template_name, context=None):
        """
        Рендерит HTML-шаблон и отправляет его клиенту.
        """
        if context is None:
            context = {}

        context.setdefault("app", app)
        context.setdefault("author", true_author)

        template = env.get_template(template_name)
        html = template.render(**context)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def handle_user(self, query):
        raw_id = query.get("id", [None])[0]
        try:
            user_id = int(raw_id)
        except (TypeError, ValueError):
            self.send_error(400, "Invalid or missing id parameter")
            return

        # Найти пользователя по ID из списка allusers
        user = next((u for u in allusers if u.id == user_id), None)
        if user is None:
            self.send_error(404, "User not found")
            return
        user_subscriptions = [uc.currency_id for uc in user_currencies if uc.user_id == user_id]
        subscribed_currencies = [currency for currency in build_currency_models(allcodes) if currency.id in user_subscriptions]


        context = {
            "app": app,
            "user": user,
            "subscriptions": subscribed_currencies,
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }

        # Рендерим шаблон с данными пользователя
        self.render_template("user.html", context)
    def handle_users(self):
        """
        Обработка маршрута /users (список пользователей).
        """
        users = allusers
        
        # Передаем данные в шаблон
        context = {
            "app": app,
            "users": users,
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }
        
        # Рендерим шаблон и отправляем в браузер
        self.render_template("users.html", context)

    def handle_currencies(self):
        """Обработка маршрута /currencies (список валют)."""
        codes = allcodes  # Список валют
        currencies = build_currency_models(codes)  # Получаем объекты валют
        
        context = {
            "app": app,
            "currencies": currencies,
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }

        self.render_template("currencies.html", context)
    
    def handle_author(self):
        """
        Обработка маршрута /author (страница с информацией об авторе).
        """
        context = {
            "app": app,
            "author": true_author,  # передаем объект автора
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }

        # Рендерим шаблон и отправляем в браузер
        self.render_template("author.html", context)

    def handle_index(self):
        """
        Обработка маршрута / (главная страница).
        """
        context = {
            "app": app,
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }
        
        self.render_template("index.html", context)
    
if __name__ == "__main__":
    server_address = ("localhost", 8000)  # Адрес и порт для сервера
    httpd = HTTPServer(server_address, MyRequestHandler)  # Создаём сервер
    print("Server started on http://localhost:8000")
    httpd.serve_forever() 