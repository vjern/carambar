import sys
import time


sys.path.append('..')
from carambar import fmt


def get_temperature():
    return 1

def get_message():
    return 'Hello!'

def get_remaining_info():
    return 'there'


def test_layout():

    my_display = (
        fmt.Layout(sep=':')
        .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_temperature)
        .field(align=fmt.MIDDLE, pack=fmt.ASIS, src=get_message)
        .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_remaining_info)
    )

    print(my_display)

    print('{:<100}'.format(my_display))


if __name__ == "__main__":
    test_layout()