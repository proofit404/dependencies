from _dependencies.exceptions import DependencyError


class _InjectorTypeType(type):
    pass


def _is_nested_injector(name, dependency):
    if isinstance(dependency, _InjectorTypeType):
        message = nested_injector_template.format(name=name)
        raise DependencyError(message)


# Messages.


nested_injector_template = """
Attribute {name!r} contains nested Injector.

Do not depend on nested injectors directly.

Use reference objects to access inner attributes of other injectors instead.
""".strip()
