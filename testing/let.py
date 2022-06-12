from textwrap import indent

import pytest

from dependencies import Package
from dependencies import value


class Let:
    def cls(self, name, *methods):
        if methods:
            methods = "\n".join([indent(method, "    ") for method in methods])
        else:
            methods = "    pass"
        return f"class {name}:\n{methods}\n"

    def fun(self, name, arg, *res):
        lines = "".join(f"    {line}\n" for line in res)
        return f"def {name}({arg}):\n{lines}\n"

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
    return Let()
