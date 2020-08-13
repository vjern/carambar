from concurrent.futures import ThreadPoolExecutor
import sys
import traceback
import threading
from functools import wraps, partial

    
TPE = ThreadPoolExecutor(max_workers=1)
map = TPE.map


def alerter(f):
    @wraps(f)
    def wrapper(*a, **kw):
        try:
            return f(*a, **kw)
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            raise
    return wrapper


def new(f, *args, **kwargs):
    tf = partial(f, *args, **kwargs)
    tf = alerter(tf)
    TPE.submit(tf)


if __name__ == "__main__":
    
    def f():
        raise ValueError

    new(f)
