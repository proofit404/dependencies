from .._spec import nested_injector, this_link
from ..exceptions import DependencyError


def check_links(class_name, dependencies):

    for argument_name, (dep, depspec) in dependencies.items():
        if depspec is this_link:
            check_links_for(
                class_name, argument_name, dependencies, dep, filter_expression(dep)
            )
        elif depspec is nested_injector:
            nested_dependencies = {"__parent__": (dependencies, None)}
            nested_dependencies.update(dep.__dependencies__)
            check_links(class_name, nested_dependencies)


def check_links_for(class_name, argument_name, dependencies, origin, expression):

    try:
        argname = next(expression)
    except StopIteration:
        return

    try:
        attribute, argspec = dependencies[argname]
    except KeyError:
        return

    if argspec is nested_injector:
        nested_dependencies = {"__parent__": (dependencies, None)}
        nested_dependencies.update(attribute.__dependencies__)
        check_links_for(
            class_name, argument_name, nested_dependencies, origin, expression
        )
    elif argname == "__parent__":
        check_links_for(class_name, argument_name, attribute, origin, expression)
    elif attribute is origin:
        raise DependencyError(
            "{0!r} is a circle link in the {1!r} injector".format(
                argument_name, class_name
            )
        )
    elif argspec is this_link:
        check_links_for(
            class_name,
            argument_name,
            dependencies,
            origin,
            filter_expression(attribute),
        )


def filter_expression(link):

    for parent in range(link.__parents__):
        yield "__parent__"

    for kind, symbol in link.__expression__:
        if kind == ".":
            yield symbol
        elif kind == "[]":
            raise StopIteration()
