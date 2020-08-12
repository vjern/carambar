import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.itqdm import tqdm


def test_itqdm():

    items = (
        time.sleep(.1) or item
        for item in range(100)
    )

    # for item in tqdm(items, total=100):
    #     print(item)

    for item in items | CaramBar('Doing stuff'):
        print(item)


if __name__ == "__main__":
    test_itqdm()