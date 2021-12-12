from importlib import import_module
from inspect import ismodule

from _dependencies.objects.attributes import _Attributes


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
    imported, attrs = _import_module(dependency.__name__, dependency.__attrs__)
    imported_spec = yield _Attributes(imported, attrs)
    return imported_spec


def _import_module(module, attrs):
    result = import_module(module)
    index = 0
    for attr in attrs:
        index += 1
        if hasattr(result, attr):
            attribute = getattr(result, attr)
            if not ismodule(attribute):
                result = attribute
                break
        module += "." + attr
        result = import_module(module)
    return result, attrs[index:]
