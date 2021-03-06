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

    result = ('{:<100}'.format(my_display))
    assert result == '1:Hello!:there', result

    #

    my_display = (
        fmt.Layout(sep=':')
        .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_temperature)
        .field(align=fmt.MIDDLE, pack=20, src=get_message)
        .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_remaining_info)
    )

    fmt.RawLayout(
        '{temp:<30}:{msg:^*}:{info:<}',
        callers={
            'temp': get_temperature,
            'msg': get_message,
            'info': get_remaining_info
        }
    )

    print(my_display)

    result = ('{:<100}'.format(my_display))
    assert result == '1:       Hello!       :there', result


def test_raw_layout():
    rlay = fmt.RawLayout(
        '{temp:<30}:{msg:^*}:{info:<}',
        temp=get_temperature,
        msg=get_message,
        info=get_remaining_info
    )


if __name__ == "__main__":
    test_layout()