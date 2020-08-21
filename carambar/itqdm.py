from . carambar import CaramBar
from . import termset
import os


def _get_cols(fp: int) -> int: 
    return termset.get_terminal_size().columns


def tqdm(*args, **kwargs):

    import tqdm  # type: ignore

    # To enable tqdm dynamic resizing
    tqdm._tqdm._environ_cols_wrapper = lambda: _get_cols

    if 'file' in kwargs:
        return tqdm.tqdm(*args, **kwargs)

    color = None
    if 'color' in kwargs:
        color = kwargs.pop('color')

    print_leftovers = kwargs.get('leave')
    
    ctxb, iostream = CaramBar.with_io(
        leave=print_leftovers,
        color=color
    )
    
    kwargs.update({
        'file': iostream,
        'dynamic_ncols': True,
        'leave': print_leftovers
    })

    with ctxb:
        tqobj = tqdm.tqdm(*args, **kwargs)
        yield from tqobj
