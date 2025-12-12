import unittest
import io
import sys
import logging
import lab7


class TestMySolution(unittest.TestCase):
    def test_correctness(self):
        # проверка корректности полученных данных
        self.assertEqual(lab7.get_currencies(["USD", "EUR", "NGN", "CNY"]), {'USD': 79.3398, 'EUR': 92.9384, 'NGN': 54.5147, 'CNY': 11.1867})
        self.assertIsInstance(lab7.get_currencies(['USD', 'EUR']), dict)
        self.assertIsInstance(lab7.get_currencies(['USD', 'EUR'])['USD'], float)
        self.assertGreaterEqual(lab7.get_currencies(['USD', 'EUR'])['USD'], 0)

    def test_custom_errors(self):
        # проверка обработки ошибок
        with self.assertRaises(KeyError):
            lab7.get_currencies(["RUB", "FAKECURRENCY"])
        with self.assertRaises(ConnectionError):
            lab7.get_currencies(["USD"], url = "https://thiswebsitedoesnotexist123456789.com")
            lab7.get_currencies(["USD"], url = "0")


class TestLogger(unittest.TestCase):

    def test_logging_to_stringio(self):
        """Проверяем ветку handle.write через StringIO."""

        stream = io.StringIO()

        @lab7.logger(handle=stream)
        def add(a, b):
            return a + b

        result = add(2, 3)
        logs = stream.getvalue()

        self.assertEqual(result, 5)
        self.assertIn("starting func add", logs)
        self.assertIn("successfully finished! result 5", logs)

    def test_logging_with_logger_info(self):
        """Проверяем ветку logging.Logger: info()."""

        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        log = logging.getLogger("test_logger_branch")
        log.handlers = []
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        log.propagate = False

        @lab7.logger(handle=log)
        def mul(a, b):
            return a * b

        result = mul(3, 4)
        logs = log_stream.getvalue()

        self.assertEqual(result, 12)
        self.assertIn("starting func mul", logs)
        self.assertIn("successfully finished! result 12", logs)

    def test_error_is_logged_and_reraised(self):
        """Проверяем, что ошибка логируется и пробрасывается дальше."""

        stream = io.StringIO()

        @lab7.logger(handle=stream)
        def boom():
            raise ValueError("kaboom")

        with self.assertRaises(ValueError):
            boom()

        logs = stream.getvalue()
        self.assertIn("ERROR: ValueError kaboom", logs)

    def test_wraps_preserves_name(self):
        """Проверяем, что functools.wraps сохраняет имя функции."""

        @lab7.logger
        def hello():
            return "ok"

        self.assertEqual(hello.__name__, "hello")


if __name__ == '__main__':
  unittest.main()