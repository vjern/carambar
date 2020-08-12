import os
import io
from contextlib import contextmanager
from functools import partial
from .typing import Optional, Union, Callable

from . import seq

"""
Compilation of terminal operations.
"""


def hide_cursor(file: io.IOBase):
    """Hide terminal cursor."""
    file.write(seq.Cursor.HIDE)


def show_cursor(file: io.IOBase):
    """Unhide terminal cursor."""
    file.write(seq.Cursor.SHOW)


def is_suitable_io_device(fileno: int) -> bool:
    """
    TODO: Give the actual reason why os.get_terminal_size throws an OSError
    when the fd is not a tty.
    """
    try:
        os.get_terminal_size(fileno)
        return True
    except OSError:
        return False


def build_sizer(fd: Optional[Union[io.IOBase, int]] = None) -> Callable:
    """
    Build a function returning the terminal size depending on the available
    and requested I/O streams.
    Try to get the terminal size of the given io stream, otherwise defaults to stdin,
    and if stdin is no tty, defaults to a fixed size of (80, 24).
    """
    if isinstance(fd, io.IOBase):
        fd = fd.fileno()
    if type(fd) is int:
        if is_suitable_io_device(fd):
            return partial(os.get_terminal_size, fd)
        return partial(os.get_terminal_size, 0)
    if fd is None and os.isatty(0):
        return partial(os.get_terminal_size, 0)
    return lambda: os.terminal_size((80, 24))


get_terminal_size = build_sizer(2)


def move_cursor_to(x: int, y: int, fio: io.IOBase):
    """Move cursor to specified position inside the terminal window."""
    fio.write(seq.Cursor.MOVE_TO.format(x=x, y=y))


@contextmanager
def ancurs(fio: io.IOBase):
    """Remember cursor position on entry, then moves cursor back to said position on exit."""
    fio.write(seq.Cursor.BIND)
    yield
    fio.write(seq.Cursor.UNBIND)


def set_scroll_region(nrows: int, fio: io.IOBase):
    """Set terminal scroll region sizein terms of rows."""
    fio.write('\n')
    with ancurs(fio):
        fio.write(seq.ScrollRegion.SET.format(0, nrows - 1))
    fio.write(seq.Cursor.goes.UP)
    fio.flush()
