import re


PREFIX = '\033'


def prefix_codes(cls):
    for key, value in vars(cls).items():
        if key.startswith('_'):
            continue
        if key != key.upper():
            continue
        if value is None:
            continue
        setattr(cls, key, PREFIX + value)
    return cls


@prefix_codes
class Color:
    @staticmethod
    def reduce(code: str) -> str:
        codes = re.finditer(PREFIX + r'\[([0-9;]*)m', code)
        codes = list(m.group(1).strip(';') for m in codes)
        if codes:
            code = ';'.join(codes)
        return code
    ANSII = '[{}m'


@prefix_codes
class Cursor:
    MOVE_TO = '[{x};{y}H'
    # MOVE_TO_H = '[{y}'
    BIND = '7'
    UNBIND = '8'
    SHOW = '[?25h'
    HIDE = '[?25l'
    @prefix_codes
    class goes:
        UP = '[A'
        UPS = '[{}A'
        DOWN = None
        LEFT = None
        RIGHT = None


@prefix_codes
class Erase:
    AFTER = '[K'
    BELOW_AFTER = '[J'
    # ALL = '[K'


@prefix_codes
class ScrollRegion:
    SET = '[{};{}r'