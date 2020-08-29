from _dependencies.exceptions import DependencyError
from _dependencies.markers import injectable


def _check_circles(dependencies):

    for depname in dependencies:
        _check_circles_for(dependencies, depname, depname)


def _check_circles_for(dependencies, attrname, origin):

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
            _check_circles_for(dependencies, name, origin)
