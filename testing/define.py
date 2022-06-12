import pytest


class Define:
    def __init__(self, coder, let):
        self.coder = coder
        self.let = let

    def require(self, module, export):
        self.coder.write(f"from {module} import {export}\n")

    def cls(self, name, *methods):
        self.coder.write(self.let.cls(name, *methods))
        return name

    def fun(self, name, arg, *res):
        self.coder.write(self.let.fun(name, arg, *res))
        return name

    def package(self, arg):
        module = arg.split(".", 1)[0]
        self.coder.write(f"{module} = Package({module!r})\n")
        return arg


@pytest.fixture()
def define(coder, let):
    """Dump defined dependencies into the test case file."""
    return Define(coder, let)
