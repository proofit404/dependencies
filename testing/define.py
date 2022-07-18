import pytest


class _Direct:
    def __init__(self, coder, let):
        self.coder = coder
        self.let = let

    def require(self, module, export):
        self.coder.write(f"from {module} import {export}\n")

    def h(self, arg):
        return self.cls(
            "Holder",
            self.let.fun("__new__", f"cls, {arg}", f"return {arg}"),
            self.let.fun("__init__", f"self, {arg}", "pass"),
        )

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


class _Package:
    def __init__(self, coder, let):
        self.coder = coder
        self.module = coder.module()
        self.direct = _Direct(self.module, let)
        self.coder.write(f"{self.module} = Package({self.module!r})\n")

    def require(self, module, export):
        self.direct.require(module, export)

    def h(self, arg):
        self.direct.h(arg)
        return f"{self.module}.Holder"

    def cls(self, name, *args):
        self.direct.cls(name, *args)
        return f"{self.module}.{name}"

    def fun(self, name, params, *args):
        self.direct.fun(name, params, *args)
        return f"{self.module}.{name}"


@pytest.fixture(params=[_Direct, _Package], ids=["direct", "package"])
def define(request, coder, let):
    """Dump defined dependencies into the test case file."""
    return request.param(coder, let)
