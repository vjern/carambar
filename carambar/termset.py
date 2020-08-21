import os
from contextlib import contextmanager
from functools import partial
from typing import Optional, Union, Callable, TextIO

from . import seq


"""
Compilation of terminal operations.
"""


def hide_cursor(file: TextIO):
    """Hide terminal cursor."""
    file.write(seq.Cursor.HIDE)


def show_cursor(file: TextIO):
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


def build_sizer(fd: Optional[Union[TextIO, int]] = None) -> Callable:
    """
    Build a function returning the terminal size depending on the available
    and requested I/O streams.
    Try to get the terminal size of the given io stream, otherwise defaults to stdin,
    and if stdin is no tty, defaults to a fixed size of (80, 24).
    """
    if fd is None:
        if os.isatty(0):
            return partial(os.get_terminal_size, 0)
    else:
        if isinstance(fd, TextIO):
            fd = fd.fileno()
        if type(fd) is int:
            if is_suitable_io_device(fd):
                return partial(os.get_terminal_size, fd)
            return partial(os.get_terminal_size, 0)
    return lambda: os.terminal_size((80, 24))


get_terminal_size = build_sizer(2)


def move_cursor_to(x: int, y: int, file: TextIO):
    """Move cursor to specified position inside the terminal window."""
    file.write(seq.Cursor.MOVE_TO.format(x=x, y=y))


@contextmanager
def ancurs(file: TextIO):
    """Remember cursor position on entry, then moves cursor back to said position on exit."""
    file.write(seq.Cursor.BIND)
    yield
    file.write(seq.Cursor.UNBIND)


def set_scroll_region(nrows: int, file: TextIO):
    """Set terminal scroll region sizein terms of rows."""
    print('Set scroll region to', nrows)
    file.write('\n')
    with ancurs(file):
        file.write(seq.ScrollRegion.SET.format(0, nrows - 1))
    file.write(seq.Cursor.goes.UP)
    file.flush()
