import sys
import time


sys.path.append('..')
from carambar.lineio import LineIO


def test_LineIO():

    leo = LineIO(callback=lambda x: print(repr(x)))

    leo.write('Hello there!')
    assert leo.getvalue() == 'Hello there!'
    leo.write(' I hail from a faraway land.')
    assert leo.getvalue() == 'Hello there! I hail from a faraway land.', leo.getvalue()
    leo.write('a\nA new line')
    assert leo.getvalue() == 'A new line'

    leo = LineIO(callback=print, size=2)
    leo.write('Hello there!')
    assert leo.getvalue() == 'Hello there!'
    leo.write(' I hail from a faraway land.')
    assert leo.getvalue() == 'Hello there! I hail from a faraway land.', leo.getvalue()
    leo.write('a\nA new line')
    assert leo.getvalue() == 'Hello there! I hail from a faraway land.a\nA new line'
    leo.write('\nxxx')
    assert leo.getvalue() == 'A new line\nxxx', leo.getvalue()


if __name__ == "__main__":
    test_LineIO()
    print('b')