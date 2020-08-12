import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.itqdm import tqdm
from carambar.mtest import Test


def test_itqdm():

    items = (
        time.sleep(.01) or item
        for item in range(100)
    )
    with Test(
        '!iterate through all items !while !{showing} '
        'the !{progress bar} at the bottom of the terminal'
    ):
        for item in tqdm(items, total=100):
            print(item)

    # with Test('iterate through all items and keep showing "Doing stuff" at the bottom of the terminal'):
    #     for item in items | CaramBar('Doing stuff'):
    #         print(item)


if __name__ == "__main__":
    test_itqdm()