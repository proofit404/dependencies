from textwrap import indent

import pytest

from dependencies import Package
from dependencies import value


class Define:
    def __init__(self, coder):
        self.coder = coder

    def resolve(self, module, export):
        self.coder.write(
            f"""
from {module} import {export}
            """
        )

    def cls(self, name, *methods):
        if methods:
            methods = "\n".join([indent(method, "    ") for method in methods])
        else:
            methods = "    pass"
        self.coder.write(
            f"""
class {name}:
{methods}
            """
        )
        return name

    def defn(self, name, arg, *res):
        self.coder.write(self.fun(name, arg, *res))
        return name

    def fun(self, name, arg, *res):
        lines = "".join(f"    {line}\n" for line in res)
        return f"""
def {name}({arg}):
{lines}
        """

    def fn(self, arg, res):
        return f"lambda {arg}: {res}"

    def this(self, arg):
        return f"this.{arg}"

    def value(self, name, arg, *res):
        function = self.fun(name, arg, *res).lstrip()
        return f"""
@value
{function}
        """

    def package(self, arg):
        module = arg.split(".", 1)[0]
        self.coder.write(
            f"""
{module} = Package({module!r})
            """
        )
        return arg


@pytest.fixture()
def let(coder):
    """Define dependencies in different ways."""
    return Define(coder)
