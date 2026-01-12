import sqlite3

class CurrencyRatesCRUD:
    def __init__(self, db_connection):
        # Принимаем подключение к базе данных как аргумент
        self.connection = db_connection
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Создаём таблицы user, currency, user_currency,
        если их ещё нет.
        """
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            );

            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                char_code TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(char_code) REFERENCES currency(char_code)

            );
            """
        )
        self.connection.commit()

    def create(self, num_code, char_code, name, value, nominal):
        """
        Добавить новую валюту в бд.
        """
        sql = """
        INSERT INTO currency (num_code, char_code, name, value, nominal)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (num_code, char_code.upper(), name, value, nominal))
        self.connection.commit()
    
    

    def user_create(self, name: str) -> int:
        sql = "INSERT INTO user(name) VALUES (?)"
        self.cursor.execute(sql, (name,))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def subscribe_user(self, user_id: int, char_code: str) -> int:
        if not isinstance(user_id, int) or user_id <= 0:
            raise TypeError("user_id должен быть положительным int")

        if not isinstance(char_code, str) or not char_code.strip():
            raise TypeError("char_code должен быть непустой строкой")

        code = char_code.strip().upper()

        # проверка пользователя
        self.cursor.execute("SELECT 1 FROM user WHERE id = ?", (user_id,))
        if self.cursor.fetchone() is None:
            raise ValueError(f"user_id={user_id} не существует")

        # проверка валюты
        self.cursor.execute("SELECT 1 FROM currency WHERE char_code = ?", (code,))
        if self.cursor.fetchone() is None:
            raise ValueError(f"currency {code} не существует")

        # запрет дублей
        self.cursor.execute(
            """
            SELECT 1 FROM user_currency
            WHERE user_id = ? AND char_code = ?
            """,
            (user_id, code),
        )
        if self.cursor.fetchone():
            raise ValueError("Подписка уже существует")

        self.cursor.execute(
            """
            INSERT INTO user_currency(user_id, char_code)
            VALUES (?, ?)
            """,
            (user_id, code),
        )
        self.connection.commit()

        return int(self.cursor.lastrowid)
    def read_currencies_by_user(self, user_id: int) -> list[tuple]:
        sql = """
        SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
        FROM currency c
        JOIN user_currency uc ON uc.char_code = c.char_code
        WHERE uc.user_id = ?
        ORDER BY c.char_code
        """
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()

    # def get_user_subscriptions(self, user_id: int) -> list[str]:
    #     self.cursor.execute(
    #         """
    #         SELECT char_code
    #         FROM user_currency
    #         WHERE user_id = ?
    #         ORDER BY char_code
    #         """,
    #         (user_id,),
    #     )
    #     return [row[0] for row in self.cursor.fetchall()]

    # def read_user_currency_links(self, user_id: int) -> list[tuple]:
    #     sql = """
    #     SELECT uc.id, uc.user_id, uc.char_code
    #     FROM user_currency uc
    #     WHERE uc.user_id = ?
    #     ORDER BY uc.id
    #     """
    #     self.cursor.execute(sql, (user_id,))
    #     return self.cursor.fetchall()

    def user_read_all(self) -> list[dict]:
        sql = """
        SELECT id, name
        FROM user
        ORDER BY id
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1],
            })
        return users

    def user_read_by_id(self, user_id: int):
        if not isinstance(user_id, int) or user_id <= 0:
            raise TypeError("user_id должен быть положительным int")

        sql = """
        SELECT id, name
        FROM user
        WHERE id = ?
        """
        self.cursor.execute(sql, (user_id,))
        row = self.cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
        }
    def read_currencies(self):
        """
        Возвращает все валюты из таблицы currency.
        """
        sql = """
        SELECT id, num_code, char_code, name, value, nominal
        FROM currency
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

    def update_by_char(self, char_code: str, new_value: float) -> None:
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        self.cursor.execute(sql, (new_value, char_code.upper()))
        if self.cursor.rowcount == 0:
            raise ValueError(f"Валюта {char_code.upper()} отсутствует в базе данных")
        self.connection.commit()

    def delete(self, currency_id):
        """
        Удалить валюту по ID.
        """
        sql = "DELETE FROM currency WHERE id = ?"
        self.cursor.execute(sql, (currency_id,))
        self.connection.commit()

    def close(self):
        """
        Закрыть соединение с базой данных.
        """
        self.connection.close()
