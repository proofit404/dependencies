from .. import _markers as markers
from ..exceptions import DependencyError


def check_loops(class_name, dependencies):

    for argument_name, argspec in dependencies.items():
        if argspec[0] is markers.this:
            check_loops_for(
                class_name,
                argument_name,
                dependencies,
                argspec[1],
                filter_expression(argspec[1]),
            )
        elif argspec[0] is markers.nested_injector:
            nested_dependencies = {
                "__parent__": (markers.injectable, dependencies, None, None)
            }
            nested_dependencies.update(argspec[1].__dependencies__)
            check_loops(class_name, nested_dependencies)


def check_loops_for(class_name, argument_name, dependencies, origin, expression):

    try:
        argname = next(expression)
    except StopIteration:
        return

    try:
        argspec = dependencies[argname]
    except KeyError:
        return

    if argspec[0] is markers.nested_injector:
        nested_dependencies = {
            "__parent__": (markers.injectable, dependencies, None, None)
        }
        nested_dependencies.update(argspec[1].__dependencies__)
        check_loops_for(
            class_name, argument_name, nested_dependencies, origin, expression
        )
    elif argname == "__parent__":
        check_loops_for(class_name, argument_name, argspec[1], origin, expression)
    elif argspec[1] is origin:
        raise DependencyError(
            "{0!r} is a circle link in the {1!r} injector".format(
                argument_name, class_name
            )
        )
    elif argspec[0] is markers.this:
        check_loops_for(
            class_name,
            argument_name,
            dependencies,
            origin,
            filter_expression(argspec[1]),
        )


def filter_expression(link):

    for kind, symbol in link.__expression__:
        if kind == ".":
            yield symbol
        elif kind == "[]":
            raise StopIteration()
