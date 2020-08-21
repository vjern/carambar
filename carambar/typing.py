# Fix for missing typing stdlib module in python 3.4

class Hint:

    def tell(self, item):
        raise NotImplementedError


class Alias(Hint):

    def __init__(self, name: str = None, args: list = ()):
        self.name = name or self.__class__.__name__
        self.args = args

    def __str__(self):
        return self.name + ('[%s]' % self.args) * bool(self.args)

    def __getitem__(self, *items):
        return self.__class__(name=self.name, args=items)


Union = Alias('Union')
Optional = Alias('Optional')
Callable = Alias('Callable')


class Supports(Alias):
    name = 'Supports'

    def __init__(self, fname: str, args: list, kwargs: dict, returns: type):
        super().__init__()
        self.fname = fname
        self.args = args
        self.kwargs = kwargs
        self.returns = returns
        self.__name__ = str(self)

    def tell(self, item):
        f = getattr(item, self.fname)
        # fetch spec then assert args, etc
        if f is None:
            return False
        return True

    def __str__(self):
        return_type = self.returns
        #
        signature = [a.__name__ for a in self.args or ()]
        if self.kwargs:
            signature += ['*']
            signature.extend('%s: %s' % (key, value.__name__) for key, value in self.kwargs.items())
        signature = ', '.join(str(a) for a in signature)
        #
        return self.name + '[ %s (%s) -> %s ]' % (self.fname, signature, return_type.__name__)


SupportsFormat = Supports('__format__', [str], None, str)
SupportsStr = Supports('__str__', None, None, str)


class Interface(Alias):
    pass


class StrFormatInterface(Interface):
    methods = {
        SupportsFormat,
        SupportsStr
    }

if __name__ == "__main__":
    u = Union[int, str]
    print(u)
    o = Optional[u]
    print(o)
    print(SupportsFormat)
    print(SupportsStr)

# if 'typing' in sys.modules:
#     from typing import *