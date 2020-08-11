import io
from .typing import Optional, Callable


class LineIO(io.TextIOBase):  # or Wrapper ?

    # encoding: str = 'utf-8'
    # _isatty: bool = True
    _isatty = True
    encoding = 'utf-8'

    def __init__(self, size: int = 1, callback: Optional[Callable] = None, delimiter: str = '\n'):
        self.size = size
        self.buffer = ''
        self.callback = callback
        self.delimiter = delimiter

    def write(self, text: str):
        # + handle carriage return;
        text = self.buffer + text
        text = text.split(self.delimiter)[-self.size:]
        text = self.delimiter.join(text)
        self.buffer = (text)

    def flush(self):
        # Called when leaving current scope because of base class
        self.callback(self.buffer)
        self.buffer = ''

    def isatty(self):
        return self._isatty

    def getvalue(self):
        return self.buffer
