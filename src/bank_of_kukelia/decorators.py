from loguru import logger
from fastapi.responses import  RedirectResponse
from jose import ExpiredSignatureError
from functools import wraps

def auth_exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExpiredSignatureError as ex:
            logger.warning(f'session expired: {ex}')
            return RedirectResponse('/about')
        except Exception as ex:
            raise ex
    return wrapper
