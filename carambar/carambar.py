import sys
import io
import os
import time
from functools import partial
from typing import Any, Optional  # does not exist

from . import termset
from . import seq
from . import lineio
from . import thread


class CaramBar:

    def __init__(
        self,
        text: Any = '===',
        file: io.TextIOBase = sys.stderr,
        medium_io: Optional[lineio.LineIO] = None,
        height: int = 1,
        leave: bool = False,
        update_every: Optional[float] = None,
        color: Optional[str] = None,
        hide_cursor: bool = True
    ):
        self.set_io(file)
        self.set_medium_io(medium_io)
        self.text = text
        self.leave = leave
        self.height = height
        self.hide_cursor = hide_cursor

        if update_every is not None and update_every <= 0:
            raise ValueError('Invalid dynamic update delay: %s' % update_every)

        self._dynamic_update_on = update_every is not None
        self._dynamic_update_delay = update_every

        color = seq.Color.reduce(color)
        self.color = seq.Color.ANSII.format(color)

    @classmethod
    def with_io(cls, *a, **kw):
        mio = lineio.LineIO()
        return cls(*a, medium_io=mio, **kw), mio

    def set_io(self, file: io.TextIOBase):
        self.file = file
        self.get_terminal_size = termset.build_sizer(file)
        self.termsize = self.get_terminal_size()
        # self.hide_cursor = True

    def set_medium_io(self, medium_io: lineio.LineIO):
        self.medium_io = medium_io
        if medium_io is None:
            return
        self.text = medium_io.getvalue()
        self.medium_io.callback = self.set_text

    def loop(self, every: float):
        while self._dynamic_update_on:
            self.print()
            time.sleep(every)

    def set_text(self, text: str):
        self.text = text
        self.print()

    def __enter__(self):

        # Hide cursor
        if self.hide_cursor:
            termset.hide_cursor(self.file)

        # Setup sroll region to exclude last row
        termset.set_scroll_region(self.termsize.lines - self.height + 1, self.file)

        # Print content text
        if self._dynamic_update_on:
            # Run 'self.loop' in thread
            thread.new(self.loop, self._dynamic_update_delay)
        else:
            self.print()

        return self

    def __exit__(self, *a):

        self._dynamic_update_on = False

        # Reset scroll region
        termset.set_scroll_region(self.termsize.lines + 1, self.file)

        # Erase terminal after & below cursor
        self.file.write(seq.Erase.BELOW_AFTER)

        # Make cursor visible again if it was hidden
        if self.hide_cursor:
            termset.show_cursor(self.file)

        # Print last version of content
        if self.leave:
            self.file.write(self.text + '\n')

        self.file.flush()

    @property
    def printable_text(self):

        relu = '{:<%s}' % self.termsize.columns
        relu = relu.format(self.text)

        if self.color is not None:
            relu = self.color + relu + seq.Color.ANSII.format(0)

        return relu

    def print(self):
        
        """
        Prints the context bar.

        The cursor is momentarily placed at the last row of the terminal
        to display the context bar, then is returned to its original position
        to keep displaying regular output at the same location.
        """

        pos = self.termsize.lines, 0

        with termset.ancurs(self.file):
            termset.move_cursor_to(*pos, fio=self.file)
            self.file.write(self.printable_text)

        self.file.flush()

    def iter(self, gen):
        with self:
            yield from gen

    __ror__ = iter
    
# TODO + Add handlers for the various signals (SIGWINCH, SIGINT, SIGTERM, etc.)
