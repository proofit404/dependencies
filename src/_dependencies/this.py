from _dependencies import markers
from _dependencies.checks.this import _check_expression
from _dependencies.exceptions import DependencyError


class This:
    """Declare attribute and item access during dependency injection."""

    def __init__(self, expression):

        self.__expression__ = expression

    def __getattr__(self, attrname):

        return This(self.__expression__ + ((".", attrname),))

    def __getitem__(self, item):

        return This(self.__expression__ + (("[]", item),))

    def __lshift__(self, num):

        if not isinstance(num, int) or num <= 0:
            raise ValueError("Positive integer argument is required")
        else:
            return This(((".", "__parent__"),) * num)


this = This(())


def _make_this_spec(dependency):

    _check_expression(dependency)
    return markers.this, _ThisSpec(dependency), {"__self__": False}, {"__self__"}, set()


class _ThisSpec:
    def __init__(self, dependency):

        self.dependency = dependency

    def __call__(self, __self__):

        result = __self__

        for kind, symbol in self.dependency.__expression__:
            if kind == ".":
                try:
                    result = getattr(result, symbol)
                except DependencyError:
                    message = (
                        "You tried to shift this more times than Injector has levels"
                    )
                    if symbol == "__parent__":
                        raise DependencyError(message)
                    else:
                        raise
            elif kind == "[]":
                result = result[symbol]

        return result

    @property
    def __expression__(self):

        return self.dependency.__expression__
