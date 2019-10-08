import importlib

from _dependencies.attributes import Replace
from _dependencies.markers import lazy_import


class Package(object):
    # FIXME: Docstring.

    def __init__(self, name):

        self.__name__ = name
        self.__attrs__ = ()

    def __getattr__(self, attrname):

        result = Package(self.__name__)
        result.__attrs__ = self.__attrs__ + (attrname,)
        return result


def make_package_spec(dependency):

    return lazy_import, ImportSpec(dependency), [], 0


class ImportSpec(object):
    def __init__(self, dependency):

        self.__name__ = dependency.__name__
        self.__attrs__ = dependency.__attrs__

    def __call__(self):

        module = self.__name__
        result = importlib.import_module(module)
        index = 0

        for attr in self.__attrs__:
            index += 1
            try:
                module += "." + attr
                result = importlib.import_module(module)
            except ImportError:
                result = getattr(result, attr)
                break

        raise Replace(result, self.__attrs__[index:])
