import io
from typing import Optional, Callable


class LineIO(io.TextIOBase):

    """
    IO-like interface that only keeps track of the last n lines of its buffer.

    :param size: The number of lines to keep in memory.
    :param callback: When flushing, the available lines are sent to the callback function.
    :param delimiter: Line delimiter.

    """

    _isatty: bool = False
    encoding: str = 'utf-8'

    def __init__(
        self,
        size: int = 1,
        callback: Optional[Callable] = None,
        delimiter: str = '\n'
    ):
        self.size = size
        self.buffer = ''
        self.callback = callback or (lambda *a: None)
        self.delimiter = delimiter

    def write(self, text: str):
        text = self.buffer + text
        text = self.delimiter.join(text.split(self.delimiter)[-self.size:])
        self.buffer = (text)

    def flush(self):
        # Called when leaving current scope because of base class
        self.callback(self.buffer)
        self.buffer = ''

    def isatty(self) -> bool:
        return self._isatty

    def getvalue(self) -> str:
        return self.buffer

    def __enter__(self):
        return self

    def __exit__(self, *a):
        # print('__exit__')
        pass
