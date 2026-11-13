import unittest
from unittest.mock import patch

from main import measure_time, timer_decorator


class TestMeasureTime(unittest.TestCase):

    def test_measure_time_returns_function_result_and_duration(self):
        def add(a, b):
            return a + b

        with patch("main.time.perf_counter", side_effect=[1.0, 2.25]):
            result, duration = measure_time(add, 5, 3)

        self.assertEqual(result, 8)
        self.assertEqual(duration, 1.25)

    def test_measure_time_passes_keyword_arguments(self):
        def greet(name, punctuation="!"):
            return f"Привіт, {name}{punctuation}"

        with patch("main.time.perf_counter", side_effect=[2.0, 3.0]):
            result, duration = measure_time(
                greet, name="Данило", punctuation="."
            )

        self.assertEqual(result, "Привіт, Данило.")
        self.assertEqual(duration, 1.0)

    def test_measure_time_reraises_function_error(self):
        def fail():
            raise ValueError("test error")

        with patch("main.time.perf_counter", side_effect=[1.0]):
            with self.assertRaisesRegex(ValueError, "test error"):
                measure_time(fail)

    def test_decorator_measures_execution_time(self):
        @timer_decorator
        def multiply(a, b):
            return a * b

        with patch("main.time.perf_counter", side_effect=[4.0, 5.5]):
            result, duration = multiply(4, 5)

        self.assertEqual(result, 20)
        self.assertEqual(duration, 1.5)

    def test_decorator_preserves_function_name(self):
        @timer_decorator
        def sample_function():
            return "ok"

        self.assertEqual(sample_function.__name__, "sample_function")


if __name__ == "__main__":
    unittest.main()
