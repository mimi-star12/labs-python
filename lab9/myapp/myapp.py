import os, sqlite3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape

from models.app import App, Author 
from models.user import User
from models.user_currency import UserCurrency
from models.currency import Currency
from utils.currencies_api import get_currencies
from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import CurrencyRatesCRUD

env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape())

conn = sqlite3.connect(":memory:", check_same_thread=False)
db = CurrencyRatesCRUD(conn)
currency_controller = CurrencyController(db)

true_author = Author('Милана Карелина')
app = App('CurrenciesListApp', 0.3, true_author)

SEED_CURRENCIES = [
    ("840", "USD", "Доллар США", 90.0, 1),
    ("978", "EUR", "Евро", 91.0, 1),
    ("156", "CNY", "Юань", 12.5, 1),
    ("392", "JPY", "Иена", 0.62, 100),
    ("826", "GBP", "Фунт стерлингов", 115.0, 1),
]

SEED_USERS = [
    "Chingiz Daddy",
    "pipi pupu",
    "Ploni Almoni",
]

SEED_SUBSCRIPTIONS = {
    "Chingiz Daddy": ["USD", "EUR"],
    "pipi pupu": ["CNY"],
    "Ploni Almoni": ["JPY", "GBP"],
}

def seed_db(db):
    # 1) валюты
    for num_code, char_code, name, value, nominal in SEED_CURRENCIES:
        db.create(num_code, char_code, name, value, nominal)

    # 2) пользователи
    user_ids = {}
    for name in SEED_USERS:
        user_id = db.user_create(name)   # этот метод нужен в db
        user_ids[name] = user_id

    # 3) подписки
    for user_name, codes in SEED_SUBSCRIPTIONS.items():
        uid = user_ids[user_name]
        for code in codes:
            db.subscribe_user(uid, code)

seed_db(db)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query, keep_blank_values=True)

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
        elif path == "/currency/show":
            self.handle_currency_show()
        elif path == "/currency/delete":
            self.handle_currency_delete(query)
        elif path == "/currency/update":
            self.handle_currency_update(query)
        else:
            self.send_error(404, "Not Found")


    def handle_static(self, path: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, path.lstrip("/"))

        if not os.path.isfile(file_path):
            self.send_error(404, "Static file not found")
            return

        if file_path.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        elif file_path.endswith(".js"):
            content_type = "application/javascript; charset=utf-8"
        else:
            content_type = "application/octet-stream"

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

    def handle_currency_update(self, query):
        if not query:
            self.send_error(400, "Missing currency code in query")
            return

        # берём первый ключ: "USD"
        char_code = next(iter(query.keys()))

        try:
            currency_controller.update_currency(char_code)
        except ValueError as e:
            self.send_error(400, str(e))
            return
        except Exception as e:
            self.send_error(500, f"Update failed: {e}")
            return

        self.send_response(302)
        self.send_header("Location", "/currencies")
        self.end_headers()

    def handle_currency_show(self):
        currencies = currency_controller.list_currencies() 
        print("Currencies from DB:")
        for c in currencies:
            print(c)

        self.send_response(302)
        self.send_header("Location", "/currencies")
        self.end_headers()

    def handle_currency_delete(self, query):
        raw_id = query.get("id", [None])[0]
        try:
            currency_id = int(raw_id)
        except (TypeError, ValueError):
            self.send_error(400, "Invalid or missing id parameter")
            return

        try:
            currency_controller.delete_currency(currency_id)
        except ValueError as e:
            self.send_error(400, str(e))
            return
        except Exception as e:
            self.send_error(409, f"Cannot delete currency id={currency_id}: {e}")
            return

        self.send_response(302)
        self.send_header("Location", "/currencies")
        self.end_headers()

    def handle_user(self, query):
        raw_id = query.get("id", [None])[0]
        try:
            user_id = int(raw_id)
        except (TypeError, ValueError):
            self.send_error(400, "Invalid or missing id parameter")
            return

        user = db.user_read_by_id(user_id)  # нужен метод в db
        if user is None:
            self.send_error(404, "User not found")
            return



        rows = db.read_currencies_by_user(user_id)

        subscriptions = [
            {
                "id": r[0],
                "num_code": r[1],
                "char_code": r[2],
                "name": r[3],
                "value": r[4],
                "nominal": r[5],
            }
            for r in rows
        ]
        context = {
            "user": user,
            "subscriptions": subscriptions,
            "navigation": [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Автор", "href": "/author"},
            ],
        }
        self.render_template("user.html", context)

    def handle_users(self):
        users = db.user_read_all()  # нужен метод в db
        self.render_template("users.html", {"users": users})

    def handle_currencies(self):
        currencies = currency_controller.list_currencies()  # из БД

        context = {
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