import inspect


class A:

    def __init__(self, a: int):
        self.a = a

    def __str__(self):
        return 'A(a=%s)' % self.a

    def __format__(self, *args):
        print(args)
        return str(self)

    
a = A(33)
print(a)
print(str(a))
print(dir(a))
print('+{:_ldfkslkflksdlfkslkdflskféç(_àç_&àç0}+'.format((a)))