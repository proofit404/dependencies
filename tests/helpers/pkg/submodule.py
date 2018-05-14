class Foo(object):

    def do(self):
        return 1


class Bar(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def do(self):
        return self.a + self.b


def function():
    return 1


variable = 1
