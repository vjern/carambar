# Fix for missing typing stdlib module in python 3.4


class Alias:

    def __init__(self, name: str, args: list = ()):
        self.name = name
        self.args = args

    def __str__(self):
        return self.name

    def __getitem__(self, *items):
        return Alias(name=self.name, args=items)


Union = Alias('Union')
Optional = Alias('Optional')
Callable = Alias('Callable')