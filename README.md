# CaramBar

## tqdm Integration

This should just be a drop-in replacement:

```py
from carambar import tqdm

for item in tqdm(items):
    ...
```

## More display options

### Not just the strings, but the objects too

A CaramBar takes a `text` object. This can be either a raw string, or any object that properly implements `__format__`:

```py
with CaramBar('Hello world!'):
    ...
```

```py
class BottomDisplay:
    def __format__(self, fmt: str) -> str:
        content = 'Some really important contextual information'
        return format(content, fmt)

with CaramBar(BottomDisplay()):
    ...
```
Together with this, you can tell the CaramBar to update its display regularly, so you get real-time information:

```py
with CaramBar(text=BottomDisplay(), update_every=1):
    ...
```
With only a function:
```py
from carambar.tools import fmtee

def get_info():
    ...

with CaramBar(fmtee(get_info)):
    ...
```
Composing a display:
```py
from carambar import fmt

my_display = (
    fmt.Layout(sep=':')
    .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_temperature)
    .field(align=fmt.MIDDLE, pack=fmt.ASIS, src=get_message)
    .field(align=fmt.LEFT, pack=fmt.ASIS, src=get_remaining_info)
)

with CaramBar(my_display):
    ...
```