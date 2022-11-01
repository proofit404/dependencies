from warnings import warn

from _dependencies.exceptions import DependencyError
from _dependencies.spec import _Spec


class This:
    """Declare attribute and item access during dependency injection."""

    def __init__(self, expression):
        self.__expression__ = expression

    def __getattr__(self, attrname):
        if attrname == "__wrapped__":
            raise AttributeError
        warn(
            "Replace this objects with package import statements",
            DeprecationWarning,
            stacklevel=2,
        )
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
    expression = dependency.__expression__
    _check_expression(expression)
    return _Spec(
        _ThisFactory(expression),
        {"__self__": False},
        {"__self__"},
        set(),
        lambda: "'this'",
        False,
    )


class _ThisFactory:
    def __init__(self, expression):
        self.expression = expression

    def __call__(self, __self__):
        operators = {".": _get_attribute, "[]": _get_item}
        result = __self__
        for operator, symbol in self.expression:
            result = operators[operator](result, symbol)
        return result, None


def _get_attribute(instance, name):
    try:
        return getattr(instance, name)
    except DependencyError:
        if name == "__parent__":
            message = "You tried to shift this more times than Injector has levels"
            raise DependencyError(message) from None
        else:
            raise


def _get_item(instance, name):
    return instance[name]


def _check_expression(expression):
    if not any(
        symbol
        for operator, symbol in expression
        if operator == "." and symbol != "__parent__"
    ):
        raise DependencyError("You can not use 'this' directly in the 'Injector'")
