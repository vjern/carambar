import sys
import io
import os
from functools import partial
# from typing import SupportsFormat
SupportsFormat = object()

from . import termset
from . import seq
from . import lineio


class CaramBar:

    def __init__(
        self,
        fio: io.IOBase = sys.stderr,
        text: str = '<3',
        medium_io: lineio.LineIO = None,
        leave: bool = False
    ):
        self.set_io(fio)
        self.set_medium_io(medium_io)
        self.text = text
        self.leave = leave

    @classmethod
    def withIO(cls, *a, **kw):
        return cls(*a, medium_io=lineio.LineIO(), **kw)

    def set_io(self, fio: io.IOBase):
        self.io = fio
        self.get_terminal_size = termset.build_sizer(fio)
        self.termsize = self.get_terminal_size()
        self._hide_cursor = True

    def set_medium_io(self, medium_io):
        self.medium_io = medium_io
        if medium_io is None:
            return
        self.text = medium_io.getvalue()
        # self.medium_io = lineio.LineIO(callback=import_fable)
        self.medium_io.callback = self.set_text

    def set_text(self, text: str):
        self.text = text
        self.print()

    def __enter__(self):

        # Hide cursor
        if self._hide_cursor:
            termset.hide_cursor(self.io)

        # Setup sroll region to exclude last row
        termset.set_scroll_region(self.termsize.lines, self.io)

        # Print content text
        self.print()

        return self

    def __exit__(self, *a):

        # Reset scroll region
        termset.set_scroll_region(self.termsize.lines + 1, self.io)

        # Erase terminal after & below cursor
        self.io.write( seq.Erase.BELOW_AFTER )

        # Make cursor visible again if it was hidden
        if self._hide_cursor:
            termset.show_cursor(self.io)

        # Print last version of content
        if self.leave:
            self.io.write(self.text)

        self.io.flush()

    @property
    def printable_text(self):
        return (
            ''
            # + seq.Color.ANSII.format(7)
            + ('{:<%s}' % self.termsize.columns).format(self.text)
            # + seq.Color.ANSII.format(0)
        )

    def print(self):
        """
        Prints the context bar.

        The cursor is momentarily placed at the last row of the terminal
        to display the context bar, then is returned to its original position
        to keep displaying regular output at the same location.
        """

        pos = self.termsize.lines, 0

        with termset.ancurs(self.io):
            termset.move_cursor_to(*pos, fio=self.io)
            self.io.write(self.printable_text)

        self.io.flush()
