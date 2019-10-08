from _dependencies.exceptions import DependencyError
from _dependencies.markers import injectable
from _dependencies.markers import nested_injector
from _dependencies.markers import this


def check_loops(class_name, dependencies):

    for attrname, spec in dependencies.items():
        if spec[0] is this:
            check_loops_for(
                class_name, attrname, dependencies, spec, filter_expression(spec)
            )
        elif spec[0] is nested_injector:
            check_loops(class_name, nested_dependencies(dependencies, spec))


def check_loops_for(class_name, attribute_name, dependencies, origin, expression):

    try:
        attrname = next(expression)
    except StopIteration:
        return

    try:
        spec = dependencies[attrname]
    except KeyError:
        return

    if spec[0] is nested_injector:
        check_loops_for(
            class_name,
            attribute_name,
            nested_dependencies(dependencies, spec),
            origin,
            expression,
        )
    elif attrname == "__parent__":
        from weakref import ReferenceType

        if isinstance(spec[1], ReferenceType):
            # FIXME: This is an ad-hoc solution for the broken
            # `Replace` problem.  See `dependencies._injector` comment
            # for more info.
            resolved_parent = spec[1]().__dependencies__
        else:
            resolved_parent = spec[1]
        check_loops_for(class_name, attribute_name, resolved_parent, origin, expression)
    elif spec is origin:
        message = "{0!r} is a circle link in the {1!r} injector"
        raise DependencyError(message.format(attribute_name, class_name))
    elif spec[0] is this:
        check_loops_for(
            class_name, attribute_name, dependencies, origin, filter_expression(spec)
        )


def filter_expression(spec):

    for kind, symbol in spec[1].__expression__:
        if kind == ".":
            yield symbol
        elif kind == "[]":
            raise StopIteration()


def nested_dependencies(parent, spec):

    result = {}
    result.update(spec[1].__dependencies__)
    result.update({"__parent__": (injectable, parent, [], 0)})
    return result
