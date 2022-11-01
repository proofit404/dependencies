from importlib import import_module
from inspect import ismodule
from warnings import warn

from _dependencies.exceptions import DependencyError
from _dependencies.objects.attributes import _Attributes


class Package:
    """Import given package during dependency injection.

    If it point to the class in the module, construct an instance of
    the class after import.

    If it point to the method of the class, provide bound method after
    construct an instance of the class after import.

    """

    def __init__(self, name, *, _DO_NOT_USE_THIS_FLAG_=True):
        if _DO_NOT_USE_THIS_FLAG_:
            warn(
                "Replace package objects with package import statements",
                DeprecationWarning,
                stacklevel=2,
            )
        _check_relative(name)
        self.__name__ = name
        self.__attrs__ = ()

    def __getattr__(self, attrname):
        result = Package(self.__name__, _DO_NOT_USE_THIS_FLAG_=False)
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


def _check_relative(name):
    if name.startswith("."):
        raise DependencyError("Do not use relative import path in Package declaration")
