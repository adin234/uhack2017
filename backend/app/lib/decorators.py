# Import global context
from flask import g
from flask import current_app as app

# Import core libraries
from .response import Response
from .error_handler import FailedRequest
# Other imports
from functools import wraps
from threading import Thread


def async(f):
    def wrapper(*args, **kwds):
        return app.pool.apply_async(f, args=args, kwds=kwds)

    return wrapper


def async_threaded(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def make_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = Response(logger=app.logger)
        # You can set custom headers here

        return func(res=response, *args, **kwargs)

    return wrapper


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            raise FailedRequest('No user indicated!', status_code=403,
                                payload='Resource requires access to authenticated users only')

        return f(*args, **kwargs)

    return decorated_function
