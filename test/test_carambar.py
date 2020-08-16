import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.mtest import Test, run_tests
from carambar.lineio import LineIO


def test_carambar():

    with Test(
        '!show !{text at}'
        ' the !bottom of the !terminal !{while printing} other things',
        'Were there no odd behaviors ?'
    ):
        with CaramBar():
            for idx, i in enumerate('abcdef'):
                print(i)
                time.sleep(.5)


def test_carambar_set_text():

    leo = LineIO()

    with Test(
        '!iter through items while !{display}ing the !{iter index} !below !{using set_text}',
        'Did the index update properly at each element and were there no odd behaviors ?'
    ):
        with CaramBar(leave=True, color='103;40') as cb:
            for idx, i in enumerate('124537'):
                print(i)
                cb.set_text(str(idx) + 'it')
                time.sleep(.5)

            
def test_carambar_io():

    cb, leo = CaramBar.with_io(leave=True)

    with Test(
        'iter through items while !{display}ing the !{iter index} !below !{using medium io}',
        'Did the index update properly at each element and were there no odd behaviors ?'
    ):
        with cb:
            for idx, i in enumerate('124537'):
                print(i)
                leo.write(str(idx) + 'it')
                leo.flush()
                time.sleep(.5)


if __name__ == "__main__":
    run_tests(globals())
