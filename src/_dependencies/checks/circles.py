# -*- coding: utf-8 -*-
from _dependencies.exceptions import DependencyError
from _dependencies.markers import injectable


def check_circles(dependencies):

    for depname in dependencies:
        check_circles_for(dependencies, depname, depname)


def check_circles_for(dependencies, attrname, origin):

    try:
        argspec = dependencies[attrname]
    except KeyError:
        return

    if argspec[0] is injectable:
        args = argspec[2]
        if origin in args:
            message = "{0!r} is a circular dependency in the {1!r} constructor"
            raise DependencyError(message.format(origin, argspec[1].__name__))
        for name in args:
            check_circles_for(dependencies, name, origin)
