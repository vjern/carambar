import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar


def test_carambar():

    with CaramBar():
        for i in 'abcdef':
            print(i)
            time.sleep(1)


if __name__ == "__main__":
    test_carambar()