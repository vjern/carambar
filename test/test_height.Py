import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.mtest import Test, run_tests


def test_height():

    with Test(
        '!show !{text at}'
        ' the !bottom of the !terminal !{while printing} other things',
        'Were there no odd behaviors ?'
    ):
        with CaramBar():
            for idx, i in enumerate('abcdef'):
                print(i)
                time.sleep(.5)


if __name__ == "__main__":
    run_tests(globals())
