import traceback
from flask import request
from functools import wraps
from spider.util.server_exception import ServerException, UNKNOWN_ERROR


def uniform_verification(check_token=True):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return {
                    'code': 0,
                    'data': result
                }
            except ServerException as e:
                return e.to_json()
            except Exception:
                traceback.print_exc()
                return UNKNOWN_ERROR.to_json()
        return inner
    return wrapper
