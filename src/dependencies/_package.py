import importlib
import random
import string

from . import _markers


class Package(object):
    # FIXME: Docstring.

    def __init__(self, name):
        self.__name__ = name

    def __getattr__(self, attrname):
        return Package(self.__name__ + "." + attrname)


def make_package_spec(dependency):

    return _markers.package, dependency, [], 0


def resolve_package_link(package, injector):

    names = package.__name__.split(".")
    modulename, attributes = names[0], names[1:]
    result = importlib.import_module(modulename)
    do_import = True

    for attrname in attributes:
        if do_import:
            try:
                modulename = modulename + "." + attrname
                result = importlib.import_module(modulename)
                continue
            except ImportError:
                do_import = False
        result = getattr(result, attrname)
        random_name = random_string()
        result = getattr(injector.let(**{random_name: result}), random_name)

    return result


def random_string():

    return "".join(random.choice(string.ascii_letters) for i in range(8))
