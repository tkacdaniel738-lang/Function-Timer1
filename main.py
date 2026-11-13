import logging
import time
from functools import wraps
from typing import Any, Callable


# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def measure_time(func: Callable, *args: Any, **kwargs: Any):
    """Виконує функцію, вимірює час її роботи та повертає результат і час."""
    start_time = time.perf_counter()
    try:
        result = func(*args, **kwargs)
    except Exception:
        logging.exception("Помилка під час виконання функції %s", func.__name__)
        raise

    execution_time = time.perf_counter() - start_time
    logging.info(
        "Функція %s виконалася за %.6f секунд",
        func.__name__,
        execution_time,
    )
    return result, execution_time


def timer_decorator(func: Callable):
    """Декоратор, який вимірює час роботи декорованої функції."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        return measure_time(func, *args, **kwargs)

    return wrapper


@timer_decorator
def calculate_sum(number: int) -> int:
    """Повертає суму чисел від 0 до number - 1."""
    return sum(range(number))


def main():
    print("=== ВИМІРЮВАЧ ЧАСУ ВИКОНАННЯ ===")
    try:
        number = int(input("Введіть ціле невід'ємне число: "))
        if number < 0:
            print("Помилка: число не може бути від'ємним.")
            return

        result, execution_time = calculate_sum(number)
        print("Результат:", result)
        print(f"Час виконання: {execution_time:.6f} секунд")
    except ValueError:
        print("Помилка: потрібно ввести ціле число.")


if __name__ == "__main__":
    main()
