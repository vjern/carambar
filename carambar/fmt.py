from typing import Callable, List, Dict, Union, Any


LEFT, MIDDLE, RIGHT = list('<^>')
ASIS, FIT = 0, '*'


class RawLayout:

    def __init__(self, fmtstr: str, **kw):
        self.fmt = fmtstr
        self.ames = kw


class Layout:

    def __init__(self, sep: str = ' '):
        self.sep = sep
        self.fields: List[Dict[str, Any]] = []

    def field(self, text: str = None, *, pack: Union[str, int] = ASIS, src: Callable, align: str = LEFT) -> 'Layout':
        self.fields.append({
            'text': text,
            'pack': pack,
            'src': src,
            'align': align
        })
        return self

    def __format__(self, fmt: str) -> str:
        size = int(fmt[1:])
        fields:     List[Dict[str, Any]] = [dict(f) for f in self.fields]
        fit_fields: List[Dict[str, Any]] = []
        remaining_size = size
        for field in fields:
            if field['text'] is not None:
                continue
            if field['pack'] is FIT:
                fit_fields.append(field)
                continue
            field['text'] = field['align'] + str(field['pack'])
            remaining_size -= field['pack']
        print(fit_fields, remaining_size)
        for field in fit_fields:
            field['text'] = field['align'] + str(remaining_size // len(fit_fields))
        fmt = self.sep.join('{:%s}' % f['text'] for f in fields)
        print('fmt =', fmt)

        return fmt.format(*(f['src']() for f in fields))


def fmtee(f: Callable) -> Layout:
    return Layout().field(pack=ASIS, src=f)
