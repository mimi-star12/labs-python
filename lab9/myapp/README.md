1. Цель работы

Целью лабораторной работы являлось:
Реализовать CRUD-операции (Create, Read, Update, Delete) для сущностей бизнес-логики приложения.
Освоить работу с базой данных SQLite в памяти (:memory:) с использованием модуля sqlite3.
Понять назначение и применение первичных (PRIMARY KEY) и внешних (FOREIGN KEY) ключей.
Реализовать архитектуру MVC с чётким разделением ответственности.
Выделить контроллеры для:
работы с базой данных,
бизнес-логики,
рендеринга HTML-страниц.
Реализовать полноценный роутер на базе BaseHTTPRequestHandler.
Отобразить пользователям валюты, на которые они подписаны.
Освоить тестирование логики с использованием unittest.mock.

2. Архитектура приложения (MVC)
В проекте используется архитектура MVC (Model–View–Controller):
Model
Модели описывают сущности предметной области и содержат только данные и валидацию:
User
Currency
UserCurrency
Author
App

Модели не работают с базой данных напрямую.
Controller
Контроллеры разделены по ответственности:
databasecontroller.py

Работа с SQLite
Создание таблиц
CRUD-операции
currencycontroller.py
Бизнес-логика валют
Обновление курса через API
Преобразование данных БД в формат для шаблонов

View
Представление реализовано через Jinja2:
index.html
author.html
users.html
user.html
currencies.html
Шаблоны отвечают только за отображение данных, без логики.


4. Работа с SQLite

Используется база данных в памяти:

sqlite3.connect(":memory:")


Это удобно для учебных целей, так как:

база создаётся заново при каждом запуске,

не требует файлов,

идеально подходит для тестирования.

4.1 Структура таблиц
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_code TEXT NOT NULL,
    char_code TEXT NOT NULL,
    name TEXT NOT NULL,
    value FLOAT,
    nominal INTEGER
);

CREATE TABLE user_currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    char_code TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

4.2 Первичные и внешние ключи

PRIMARY KEY

Уникально идентифицирует запись.

Используется для связи таблиц.

FOREIGN KEY

Обеспечивает ссылочную целостность.

Не позволяет создать подписку на несуществующего пользователя.

5. CRUD для Currency
Create
Добавление валюты в БД:
INSERT INTO currency (num_code, char_code, name, value, nominal)
VALUES (?, ?, ?, ?, ?)

Read
Получение всех валют:
SELECT id, num_code, char_code, name, value, nominal FROM currency

Update
Обновление курса валюты через API:
UPDATE currency SET value = ? WHERE char_code = ?

Delete
Удаление валюты:
DELETE FROM currency WHERE id = ?


Все запросы параметризованы, что защищает от SQL-инъекций.

6. Маршруты приложения
Маршрут	Назначение
/	Главная страница
/author	Информация об авторе

/users	Список пользователей
<img width="2880" height="1704" alt="image" src="https://github.com/user-attachments/assets/50d34ecc-0bed-461b-9bda-9dfb1bfc90e2" />

/user?id=...	Просмотр пользователя
<img width="2880" height="1704" alt="image" src="https://github.com/user-attachments/assets/19be1076-7ecc-4dda-a118-780845d530db" />

/currencies	Список валют
<img width="2880" height="1704" alt="image" src="https://github.com/user-attachments/assets/34936f5b-9ce4-4be0-aab1-c7623db90824" />

/currency/delete?id=...	Удаление валюты

/currency/update?USD=	Обновление курса
<img width="2880" height="1704" alt="image" src="https://github.com/user-attachments/assets/93bf22e8-ffb4-4719-8288-e3f6a8aec60c" />

/currency/show	Вывод валют в консоль

8. Подписки пользователей на валюты

Связь пользователей и валют реализована через таблицу user_currency.

Для получения подписок пользователя используется запрос:

SELECT char_code
FROM user_currency
WHERE user_id = ?


После этого валюты подгружаются из таблицы currency и отображаются на странице пользователя.

8. Тестирование (unittest.mock)

Для тестирования используется unittest и MagicMock.

Пример теста CurrencyController
def test_list_currencies(self):
    mock_db = MagicMock()
    mock_db._read_currencies.return_value = [
        (1, "840", "USD", "Доллар США", 90, 1)
    ]

    controller = CurrencyController(mock_db)
    result = controller.list_currencies()

    self.assertEqual(result[0]["char_code"], "USD")
    mock_db._read_currencies.assert_called_once()

9. Выводы
В ходе лабораторной работы:

Реализована полноценная архитектура MVC.

Освоена работа с SQLite в памяти.

Реализованы CRUD-операции с защитой от SQL-инъекций.

Реализована бизнес-логика обновления валют через API.

Настроен полноценный HTTP-роутер.

Освоено модульное тестирование с использованием mock-объектов.

Приложение масштабируемо и легко расширяется.

