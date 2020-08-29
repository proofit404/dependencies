from _dependencies.exceptions import DependencyError


def _check_expression(dependency):

    if not any(
        symbol
        for kind, symbol in dependency.__expression__
        if kind == "." and symbol != "__parent__"
    ):
        raise DependencyError("You can not use 'this' directly in the 'Injector'")
