import pytest


class _Define:
    def __init__(self, coder, let):
        self.coder = coder
        self.let = let

    def require(self, module, export):
        self.coder.write(f"from {module} import {export}\n")

    def cls(self, name, *args):
        result = self.let.cls(name, *args)
        self.coder.write(result)
        result.defined = True
        return result

    def fun(self, name, params, *args):
        result = self.let.fun(name, params, *args)
        self.coder.write(result)
        result.defined = True
        return result

    def package(self, arg):
        module = arg.split(".", 1)[0]
        self.coder.write(f"{module} = Package({module!r})\n")
        return arg

    def h(self, arg):
        result = self.cls(
            "Holder",
            self.let.fun("__new__", f"cls, {arg}", f"return {arg}"),
            self.let.fun("__init__", f"self, {arg}", "pass"),
        )
        return result


@pytest.fixture()
def define(coder, let):
    """Dump defined dependencies into the test case file."""
    return _Define(coder, let)
