from ..exceptions import DependencyError


def check_circles(dependencies):

    for depname in dependencies:
        check_circles_for(dependencies, depname, depname)


def check_circles_for(dependencies, attrname, origin):

    try:
        attribute_spec = dependencies[attrname]
    except KeyError:
        return

    attribute, argspec = attribute_spec
    if argspec:
        args = argspec[0]
        if origin in args:
            message = "{0!r} is a circular dependency in the {1!r} constructor"
            raise DependencyError(message.format(origin, attribute.__name__))

        for name in args:
            check_circles_for(dependencies, name, origin)
