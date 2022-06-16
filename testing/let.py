from textwrap import indent

import pytest


class _Class:
    def __init__(self, name, *args):
        self.name = name
        self.args = args
        self.defined = False

    def __str__(self):
        return f"class {self.name}{self.bases}:\n{self.methods}\n"

    @property
    def bases(self):
        if self.args:
            bases = [base.name for base in self.args if isinstance(base, _Class)]
            if bases:
                return "(" + ", ".join(bases) + ")"
        return ""

    @property
    def methods(self):
        if self.args:
            return "\n".join(
                [
                    indent(method, "    ")
                    for method in self.args
                    if isinstance(method, _Function)
                ]
            )
        else:
            return "    pass"

    def __contains__(self, thing):
        assert thing == "\n"
        return True


class _Function:
    def __init__(self, name, params, *args):
        self.name = name
        self.params = params
        self.args = args
        self.decorators = ""
        self.defined = False

    def dec(self, *names):
        assert not self.defined
        for name in names:
            self.decorators += f"@{name}\n"
        return self

    def __str__(self):
        return f"{self.decorators}def {self.name}({self.params}):\n{self.lines}\n"

    @property
    def lines(self):
        return "".join(f"    {line}\n" for line in self.args)

    def __contains__(self, thing):
        assert thing == "\n"
        return True

    def splitlines(self, *args):
        return str(self).splitlines(*args)


class _Let:
    def cls(self, name, *args):
        return _Class(name, *args)

    def fun(self, name, params, *args):
        return _Function(name, params, *args)

    def fn(self, arg, res):
        return f"lambda {arg}: {res}"

    def dec(self, *arg):
        *decorators, function = arg
        assert decorators
        applied = ["@{decorator}" for decorator in decorators]
        applied.append(function)
        return "\n".join(applied)

    def this(self, arg):
        return f"this.{arg}"


@pytest.fixture()
def let():
    """Define dependencies in different ways."""
    return _Let()
