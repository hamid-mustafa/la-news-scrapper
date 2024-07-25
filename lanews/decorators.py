from functools import wraps
from selenium.common import StaleElementReferenceException, TimeoutException


def retry(retries=2):
    """
    A decorator that retries a function up to a specified number of times with a delay between attempts.

    :param retries: Number of retry attempts.
    :return: The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            attempt = 0
            while attempt <= retries:
                try:
                    return func(*args, **kwargs)
                except (StaleElementReferenceException, TimeoutException) as e:
                    attempt += 1
                    if attempt > retries:
                        raise
                    self.browser.reload_page()
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
        return wrapper
    return decorator
