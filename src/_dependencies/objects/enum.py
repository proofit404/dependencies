from enum import Enum
from inspect import isclass

from _dependencies.exceptions import DependencyError


def _is_enum(name, dependency):
    if (
        not name.endswith("_class")
        and isclass(dependency)
        and issubclass(dependency, Enum)
    ):
        message = enum_template.format(name=name)
        raise DependencyError(message)


# Messages.


enum_template = """
Attribute {name!r} contains Enum.

Do not inject enumeration classes.

It will be unable to instantiate this class.

Inject its members instead.
""".strip()
