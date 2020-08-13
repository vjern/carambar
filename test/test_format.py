import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.mtest import Test


def test_format():

    import random
    import string

    class A:
        def __format__(self, info: str):
            info = info[1:]
            relu = string.printable[5:random.randrange(20) + 5]
            return '{{:{info}}}'.format(info=info).format(relu)

    obj = A()

    with Test(
        '!print some letters while showing !{a random sequence} '
        'of letters !{every 1 second} at the bottom of the terminal'
    ):
        with CaramBar(obj, color='103;95', update_every=1) as cb:
            for idx, i in enumerate('abcdef'):
                print(i)
                time.sleep(1)


if __name__ == "__main__":
    test_format()
