import pytest

from dependencies import Package
from dependencies import this
from dependencies import value


class Define:
    def resolve(self, module, export):
        code = f"from {module} import {export}"

    def cls(self, name, *methods):
        if methods:
            methods = "".join([f"    {method}\n" for method in methods])
        else:
            methods = "    pass"
        code = f"""
class {name}:
{methods}
        """
        scope = {}
        exec(code, scope)
        return scope[name]

    def defn(self, name, arg, res):
        return f"def {name}({arg}): {res}"

    def fn(self, arg, res):
        code = f"result = lambda {arg}: {res}"
        scope = {}
        exec(code, scope)
        return scope["result"]

    def integer(self):
        return 1

    def this(self, arg):
        code = f"result = this.{arg}"
        scope = {"this": this}
        exec(code, scope)
        return scope["result"]

    def value(self):
        @value
        def a():
            return 1

        return a

    def package(self, arg):
        module, tail = arg.split(".", 1)
        code = f"""
{module} = Package({module!r})
result = {module}.{tail}
        """.strip()
        scope = {"Package": Package}
        exec(code, scope)
        return scope["result"]


@pytest.fixture()
def let():
    """Define dependencies in different ways."""
    return Define()