from _dependencies.checks.this import _check_expression
from _dependencies.exceptions import DependencyError
from _dependencies.spec import _Spec


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


def _is_this(name, dependency):
    return isinstance(dependency, This)


def _build_this_spec(name, dependency):
    _check_expression(dependency)
    return _Spec(_ThisFactory(dependency), {"__self__": False}, {"__self__"}, set())


class _ThisFactory:
    def __init__(self, dependency):
        self.dependency = dependency

    def __call__(self, __self__):
        result = __self__
        for op, symbol in self.dependency.__expression__:
            result = ops[op](result, symbol)
        return result


def _get_attribute(instance, name):
    try:
        return getattr(instance, name)
    except DependencyError:
        if name == "__parent__":
            raise DependencyError(
                "You tried to shift this more times than Injector has levels"
            )
        else:
            raise


def _get_item(instance, name):
    return instance[name]


ops = {
    ".": _get_attribute,
    "[]": _get_item,
}
