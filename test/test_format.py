import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar


def test_format():

    import random
    import string

    class A:
        def __format__(self, info: str):
            info = info[1:]
            relu = string.printable[5:random.randrange(20) + 5]
            return '{{:{info}}}'.format(info=info).format(relu)

    obj = A()

    with CaramBar(obj, color='103;95', update_every=1) as cb:
    # with CaramBar(A).
        for idx, i in enumerate('abcdef'):
            print(i)
            time.sleep(1)

if __name__ == "__main__":
    test_format()
