import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.mtest import Test


def test_iter():

    items = (
        time.sleep(.01) or item
        for item in range(100)
    )

    with Test(
        '!iterate through all items and keep !{show}ing !{"Doing stuff"} '
        'at the !bottom of the !terminal'
    ):
        for item in items | CaramBar('Doing stuff'):
            print(item)


if __name__ == "__main__":
    test_iter()