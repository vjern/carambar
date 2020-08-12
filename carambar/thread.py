from concurrent.futures import ThreadPoolExecutor
import sys
import traceback
import threading
from functools import wraps, partial

    
TPE = ThreadPoolExecutor(max_workers=1)
map = TPE.map


def alerter(f):
    @wraps(f)
    def wrapper():
        try:
            return f()
        except Exception as e:
            # print(
            #     'Exception raised in thread %s:' % threading.get_ident(),
            #     type(e).__qualname__,
            #     e,
            #     file=sys.stderr
            # )
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