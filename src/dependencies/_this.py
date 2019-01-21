from . import _markers
from .exceptions import DependencyError


class This(object):
    """Declare attribute and item access during dependency injection."""

    def __init__(self, parents, expression):

        self.__parents__ = parents
        self.__expression__ = expression

    def __getattr__(self, attrname):

        return This(self.__parents__, self.__expression__ + [(".", attrname)])

    def __getitem__(self, item):

        # TODO: Do we protect against `this['foo']` expression.
        return This(self.__parents__, self.__expression__ + [("[]", item)])

    def __lshift__(self, num):

        if not isinstance(num, int) or num <= 0:
            raise ValueError("Positive integer argument is required")
        else:
            return This(self.__parents__ + num, self.__expression__)


def make_this_spec(dependency):

    check_expression(dependency)
    return _markers.this, dependency, [], 0


def check_expression(dependency):

    if not dependency.__expression__:
        raise DependencyError("You can not use 'this' directly in the 'Injector'")


def resolve_this_link(this, injector):

    result = injector

    for parent in range(this.__parents__):
        try:
            result = result.__parent__
        except DependencyError:
            raise DependencyError(
                "You tries to shift this more times that Injector has levels"
            )

    for kind, symbol in this.__expression__:
        if kind == ".":
            result = getattr(result, symbol)
        elif kind == "[]":
            result = result[symbol]

    return result


this = This(0, [])
