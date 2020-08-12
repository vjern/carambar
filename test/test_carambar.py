import sys
import time


sys.path.append('..')
from carambar.carambar import CaramBar
from carambar.lineio import LineIO


def test_carambar():

    with CaramBar():
        for idx, i in enumerate('abcdef'):
            print(i)
            time.sleep(1)


def test_carambar_set_text():

    leo = LineIO()

    with CaramBar() as cb:
        for idx, i in enumerate('124537'):
            print(i)
            cb.set_text(f'{idx}it')
            time.sleep(1)

            
def test_carambar_io():

    leo = LineIO()

    with CaramBar(mio=leo) as cb:
        for idx, i in enumerate('124537'):
            print(i)
            # cb.set_text(f'{idx}it')
            leo.write(str(idx))
            leo.flush()
            time.sleep(1)

    with CaramBar.withIO() as cb:
        leo = cb.mio
        for idx, i in enumerate('124537'):
            print(i)
            leo.write(str(idx))
            leo.flush()
            time.sleep(1)

    print('\033[J')


if __name__ == "__main__":
    test_carambar()
    # test_carambar_set_text()
    # test_carambar_io()