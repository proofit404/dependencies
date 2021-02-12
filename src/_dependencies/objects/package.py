from importlib import import_module

from _dependencies.objects.attributes import _Attributes
from _dependencies.replace import _Replace
from _dependencies.spec import _Spec


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


def _is_package(name, dependency):
    return isinstance(dependency, Package)


def _build_package_spec(name, dependency):
    return _Spec(_ImportFactory(dependency), {}, set(), set())


class _ImportFactory:
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
        raise _Replace(_Attributes(result, self.__attrs__[index:]))
