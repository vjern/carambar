from .carambar import CaramBar
import os


def _get_cols(fp): 
    return os.get_terminal_size(0).columns


def tqdm(*args, **kwargs):

    import tqdm

    # To enable tqdm dynamic resizing
    tqdm._tqdm._environ_cols_wrapper = lambda: _get_cols

    if 'file' in kwargs:
        return tqdm.tqdm(*args, **kwargs)

    else:

        print_leftovers = kwargs.get('leave')
        
        ctx, iostream = CaramBar.withIO(
            leave=print_leftovers
        )
        
        kwargs['file'] = iostream
        # kwargs['ncols'] = kwargs.get('ncols') or get_terminal_size().columns
        kwargs['dynamic_ncols'] = True

        with ctx:
            tqobj = tqdm.tqdm(*args, leave=True, **kwargs)
            yield from tqobj
