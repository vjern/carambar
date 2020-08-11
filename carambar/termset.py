import os
import io
from contextlib import contextmanager
from functools import partial
from typing import Optional, Union, Callable

from . import seq


def hide_cursor(fio: io.IOBase):
    fio.write( seq.Cursor.HIDE )


def show_cursor(fio: io.IOBase):
    fio.write( seq.Cursor.SHOW )


def is_suitable_io_device(fileno: int) -> bool:
    try:
        os.get_terminal_size(fileno)
        return True
    except OSError:
        return False


def build_sizer(i: Optional[Union[io.IOBase, int]] = None) -> Callable:
    if isinstance(i, io.IOBase):
        return build_sizer(i.fileno())
    if type(i) is int:
        if is_suitable_io_device(i):
            return partial(os.get_terminal_size, i)
        return partial(os.get_terminal_size, 0)
    if i is None is os.isatty(0):
        return partial(os.get_terminal_size, 0)
    return lambda: 100


def move_cursor_to(x: int, y: int, fio: io.IOBase):
    """Move terminal cursor to specified position."""
    fio.write( seq.Cursor.MOVE_TO.format(x=x, y=y) )


@contextmanager
def ancurs(fio: io.IOBase):
    """Remember cursor position at entry time, then moves cursor back to said position."""
    fio.write( seq.Cursor.BIND )
    yield
    fio.write( seq.Cursor.UNBIND )


def set_scroll_region(nrows: int, fio: io.IOBase):
    fio.write('\n')
    with ancurs(fio):
        fio.write( seq.ScrollRegion.SET.format(0, nrows - 1) )
    fio.write( seq.Cursor.goes.UP )
    fio.flush()
