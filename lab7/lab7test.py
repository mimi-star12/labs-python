"""HTTP подменяется; логика обработки ответа и логирование выполняются реально."""

import io
import json
import logging
import unittest
from unittest.mock import patch

import lab7


class TestCurrencies(unittest.TestCase):
    def setUp(self):
        # Фиксированные учебные данные, не текущие курсы валют.
        self.payload = {
            "Date": "2025-01-01T11:30:00+03:00",
            "PreviousDate": "2024-12-31T11:30:00+03:00",
            "PreviousURL": "https://example.test/previous.json",
            "Timestamp": "2025-01-01T12:00:00+03:00",
            "Valute": {
                "USD": {
                    "ID": "R01235", "NumCode": "840", "CharCode": "USD",
                    "Nominal": 1, "Name": "Доллар США", "Value": 90.5,
                    "Previous": 90.0,
                },
                "EUR": {
                    "ID": "R01239", "NumCode": "978", "CharCode": "EUR",
                    "Nominal": 1, "Name": "Евро", "Value": 100.25,
                    "Previous": 100.0,
                },
            },
        }
        get_patcher = patch.object(lab7.requests, "get")
        self.mock_get = get_patcher.start()
        self.addCleanup(get_patcher.stop)
        self.set_response(self.payload)

    def set_response(self, payload, status=200):
        # Настоящий Response сохраняет поведение json/raise_for_status.
        response = lab7.requests.Response()
        response.status_code = status
        response.url = "https://example.test/rates.json"
        response.encoding = "utf-8"
        response._content = json.dumps(payload).encode("utf-8")
        self.mock_get.return_value = response

    def test_returns_requested_rates(self):
        self.assertEqual(lab7.get_currencies(["USD", "EUR"]),
                         {"USD": 90.5, "EUR": 100.25})

    def test_does_not_return_unrequested_currency(self):
        self.assertEqual(lab7.get_currencies(["EUR"]), {"EUR": 100.25})

    def test_empty_currency_list_returns_empty_dict(self):
        self.assertEqual(lab7.get_currencies([]), {})

    def test_unknown_currencies_raise_independently(self):
        for code in ("RUB", "FAKECURRENCY"):
            with self.subTest(code=code):
                with self.assertRaises(KeyError):
                    lab7.get_currencies([code])

    def test_missing_valute_section_raises(self):
        del self.payload["Valute"]
        self.set_response(self.payload)
        with self.assertRaises(KeyError):
            lab7.get_currencies(["USD"])

    def test_missing_value_field_raises(self):
        del self.payload["Valute"]["USD"]["Value"]
        self.set_response(self.payload)
        with self.assertRaises(KeyError):
            lab7.get_currencies(["USD"])

    def test_non_numeric_rates_raise_independently(self):
        for value in ("90.5", None, [], {}):
            with self.subTest(value=value):
                self.payload["Valute"]["USD"]["Value"] = value
                self.set_response(self.payload)
                with self.assertRaises(TypeError):
                    lab7.get_currencies(["USD"])

    def test_integer_rate_is_supported(self):
        self.payload["Valute"]["USD"]["Value"] = 90
        self.set_response(self.payload)
        self.assertEqual(lab7.get_currencies(["USD"]), {"USD": 90})

    def test_invalid_json_raises(self):
        self.mock_get.return_value._content = b"not valid JSON"
        with self.assertRaises(ValueError):
            lab7.get_currencies(["USD"])

    def test_http_errors_become_connection_errors(self):
        for status in (404, 500):
            with self.subTest(status=status):
                self.set_response(self.payload, status=status)
                with self.assertRaises(ConnectionError):
                    lab7.get_currencies(["USD"])

    def test_network_failure_becomes_connection_error(self):
        self.mock_get.side_effect = lab7.requests.exceptions.ConnectionError("offline")
        with self.assertRaises(ConnectionError):
            lab7.get_currencies(["USD"])

    def test_timeout_becomes_connection_error(self):
        self.mock_get.side_effect = lab7.requests.exceptions.Timeout("timed out")
        with self.assertRaises(ConnectionError):
            lab7.get_currencies(["USD"])

    def test_invalid_url_becomes_connection_error(self):
        self.mock_get.side_effect = lab7.requests.exceptions.MissingSchema("bad URL")
        with self.assertRaises(ConnectionError):
            lab7.get_currencies(["USD"], url="0")

    def test_custom_url_is_forwarded(self):
        custom_url = "https://example.test/custom.json"
        self.assertEqual(lab7.get_currencies(["USD"], url=custom_url), {"USD": 90.5})
        self.mock_get.assert_called_once_with(custom_url)


class TestLogger(unittest.TestCase):
    def make_logger(self):
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
        # Независимый Logger не меняет глобальные настройки приложения.
        log = logging.Logger("lab7-test", level=logging.INFO)
        log.addHandler(handler)
        self.addCleanup(handler.close)
        self.addCleanup(log.removeHandler, handler)
        return log, stream

    def test_logging_to_stringio(self):
        stream = io.StringIO()

        @lab7.logger(handle=stream)
        def add(a, b):
            return a + b

        self.assertEqual(add(2, 3), 5)
        self.assertIn("starting func add", stream.getvalue())
        self.assertIn("result 5", stream.getvalue())

    def test_logging_with_logger_info(self):
        log, stream = self.make_logger()

        @lab7.logger(handle=log)
        def mul(a, b):
            return a * b

        self.assertEqual(mul(3, 4), 12)
        self.assertIn("INFO:starting func mul", stream.getvalue())
        self.assertIn("result 12", stream.getvalue())

    def test_stream_logs_and_reraises_same_exception(self):
        stream = io.StringIO()
        error = ValueError("kaboom")

        @lab7.logger(handle=stream)
        def boom():
            raise error

        with self.assertRaises(ValueError) as caught:
            boom()
        self.assertIs(caught.exception, error)
        self.assertIn("ERROR: ValueError kaboom", stream.getvalue())
        self.assertNotIn("successfully finished", stream.getvalue())

    def test_logger_logs_and_reraises_same_exception(self):
        log, stream = self.make_logger()
        error = ValueError("kaboom")

        @lab7.logger(handle=log)
        def boom():
            raise error

        with self.assertRaises(ValueError) as caught:
            boom()
        self.assertIs(caught.exception, error)
        self.assertIn("ERROR:ERROR: ValueError kaboom", stream.getvalue())
        self.assertNotIn("successfully finished", stream.getvalue())

    def test_keyword_arguments_and_none_result_are_preserved(self):
        stream = io.StringIO()
        received = []

        @lab7.logger(handle=stream)
        def remember(value, *, label):
            received.append((value, label))

        self.assertIsNone(remember(7, label="sample"))
        self.assertEqual(received, [(7, "sample")])
        self.assertIn("result None", stream.getvalue())

    def test_both_decorator_forms_preserve_metadata(self):
        def hello():
            """Example docstring."""
            return "ok"

        for decorate in (lab7.logger, lab7.logger(handle=io.StringIO())):
            with self.subTest(decorator=decorate):
                wrapped = decorate(hello)
                self.assertEqual(wrapped.__name__, "hello")
                self.assertEqual(wrapped.__doc__, "Example docstring.")
                self.assertIs(wrapped.__wrapped__, hello)


if __name__ == "__main__":
    unittest.main()
