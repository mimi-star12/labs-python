Лабораторная работа: Создание простого клиент-серверного приложения на Python
Цель работы

Целью данной лабораторной работы является создание простого клиент-серверного приложения с использованием стандартного Python HTTPServer. В процессе работы будет освоена маршрутизация запросов, использование шаблонизатора Jinja2 для отображения данных, а также реализация функциональности подписки пользователей на валюты с отображением их динамики изменения.

Описание предметной области
Модели

В приложении используются следующие модели:

Author

name — имя автора

group — учебная группа

App

name — название приложения

version — версия приложения

author — объект Author

User

id — уникальный идентификатор пользователя

name — имя пользователя

Currency

id — уникальный идентификатор валюты

num_code — цифровой код

char_code — символьный код

name — название валюты

value — курс валюты

nominal — номинал (за сколько единиц валюты указан курс)

UserCurrency

user_id — внешний ключ к User

currency_id — внешний ключ к Currency

Эта модель реализует связь "много ко многим" между пользователями и валютами.

Структура проекта

Проект состоит из следующих компонентов:

myapp/
├── models/
│   ├── __init__.py
│   ├── author.py
│   ├── app.py
│   ├── user.py
│   ├── currency.py
│   └── user_currency.py
├── templates/
│   ├── index.html
│   ├── users.html
│   ├── currencies.html
│   └── user.html
├── static/
│   └── css/
│       └── style.css
├── myapp.py
└── utils/
    └── currencies_api.py  # Функция get_currencies

Описание реализации
Модели

Все модели реализованы как классы с использованием геттеров и сеттеров для атрибутов.

Author - Класс для хранения информации об авторе.

App - Класс приложения, который содержит информацию о названии, версии и авторе.

User - Класс для пользователей. Каждый пользователь имеет уникальный id и имя.

Currency - Класс валюты с аттрибутами, такими как id, num_code, char_code, name, value, nominal.

UserCurrency - Модель связи между пользователем и валютой. Она реализует связь "многие ко многим".

HTTP Server и маршрутизация

Для реализации сервера используется стандартный HTTPServer и BaseHTTPRequestHandler. Сервер поддерживает следующие маршруты:

/ — главная страница с информацией о приложении и авторе.

/users — страница со списком пользователей.

/user?id=... — страница с информацией о конкретном пользователе и его подписках.

/currencies — страница со списком валют.

/author — информация об авторе.

Для рендеринга HTML используется шаблонизатор Jinja2.

env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape())

Шаблоны

index.html — главная страница.

users.html — список пользователей.

currencies.html — список валют.

user.html — информация о пользователе и его подписках.

Пример шаблона index.html:

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{{ app.name }}</title>
</head>
<body>
    <h1>{{ app.name }}</h1>
    <p>Автор: {{ author.name }}</p>
    <p>Версия: {{ app.version }}</p>

    <h2>Навигация</h2>
    <nav>
        <ul>
            {% for item in navigation %}
                <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
            {% endfor %}
        </ul>
    </nav>
</body>
</html>

Функция get_currencies

Функция get_currencies используется для получения актуальных курсов валют. Она вызывает API ЦБ РФ и возвращает значения валют.

def build_currency_models(codes):
    rates = get_currencies(codes)
    currencies = []
    for code in codes:
        value = rates.get(code)
        if value is None:
            continue
        currency = Currency(
            currency_id=code,
            num_code=0,
            char_code=code,
            name=code,
            value=value,
            nominal=1,
        )
        currencies.append(currency)
    return currencies

Рендеринг данных

Каждый маршрут обрабатывается соответствующей функцией, которая передает данные в шаблон и рендерит его с использованием Jinja2.

def render_template(self, template_name, context=None):
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

Тестирование

Тестирование моделей:

Проверка геттеров и сеттеров для всех моделей.

Проверка выброса исключений при некорректных значениях.

Тестирование функции get_currencies:

Проверка корректного получения данных с API.

Проверка обработки ошибок, таких как отсутствие валюты или проблемы с сетью.

Тестирование контроллера:

Проверка корректного ответа на запросы /users, /user?id=..., /currencies.

Тестирование шаблонов:

Убедиться, что переменные корректно передаются в шаблон и рендерятся.

Пример работы приложения

Главная страница (/): Информация о приложении и авторе.

Список пользователей (/users): Отображение всех пользователей.

Информация о пользователе (/user?id=...): Данные о пользователе и его подписках.

Список валют (/currencies): Отображение списка валют с актуальными курсами.

Выводы

Проблемы, возникшие при реализации:

Трудности при организации взаимодействия между различными моделями и запросами к API.

Трудности при обработке данных из API.

Применение принципов MVC:

Модели: Определены классы для User, Currency, UserCurrency, App и Author.

Представление: Использован шаблонизатор Jinja2 для рендеринга HTML.

Контроллер: HTTP сервер на основе BaseHTTPRequestHandler.