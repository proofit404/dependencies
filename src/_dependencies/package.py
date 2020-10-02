from importlib import import_module

from _dependencies.attributes import _Replace
from _dependencies.markers import lazy_import


class Package:
    """Import given package during dependency injection.

    If it point to the class in the module, construct an instance of
    the class after import.

    If it point to the method of the class, provide bound method after
    construct an instance of the class after import.

    """

    def __init__(self, name):

        self.__name__ = name
        self.__attrs__ = ()

    def __getattr__(self, attrname):

        result = Package(self.__name__)
        result.__attrs__ = self.__attrs__ + (attrname,)
        return result


def _make_package_spec(dependency):

    return lazy_import, _ImportSpec(dependency), {}, set(), set()


class _ImportSpec:
    def __init__(self, dependency):

        self.__name__ = dependency.__name__
        self.__attrs__ = dependency.__attrs__

    def __call__(self):

        module = self.__name__
        result = import_module(module)
        index = 0

        for attr in self.__attrs__:
            index += 1
            try:
                module += "." + attr
                result = import_module(module)
            except ImportError:
                result = getattr(result, attr)
                break

        raise _Replace(result, self.__attrs__[index:])
