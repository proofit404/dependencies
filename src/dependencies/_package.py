import importlib

from ._this import random_string


class Package(object):
    def __init__(self, name):
        self.__name = name

    def __getattr__(self, attrname):
        return Package(self.__name + "." + attrname)


def resolve_package_link(package, injector):

    names = package._Package__name.split(".")
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
