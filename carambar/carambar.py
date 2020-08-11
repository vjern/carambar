import sys
import io
import os

from . import termset
from . import seq


class CaramBar:

    def __init__(self, fileno: io.IOBase = sys.stderr):
        self.set_io(fileno)

    def set_io(self, fileno: io.IOBase):
        self.io = fileno
        self.get_terminal_size = termset.build_sizer(fileno)
        self.termsize = self.get_terminal_size()
        self._hide_cursor = True

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
        # if self.leave:
        #     self.io.write(self.text)

        self.io.flush()

    @property
    def text(self):
        return seq.Color.ANSII.format(103) + '<3' + seq.Color.ANSII.format(0)

    def print(self):
        """
        Prints the context bar.

        The cursor is momentarily placed at the last row of the terminal
        to display the context bar, then is returned to its original position
        to keep displaying regular output at the same location.
        """

        pos = self.termsize.lines, 0

        with termset.ancurs(self.io):
            termset.move_cursor_to(*pos, self.io)
            self.io.write(self.text)

        self.io.flush()