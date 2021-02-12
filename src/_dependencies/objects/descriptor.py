from inspect import isdatadescriptor
from inspect import ismethoddescriptor

from _dependencies.exceptions import DependencyError


def _is_descriptor(name, dependency):
    if ismethoddescriptor(dependency) or isdatadescriptor(dependency):
        message = descriptor_template.format(name=name)
        raise DependencyError(message)


# Messages.


descriptor_template = """
Attribute {name!r} contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
""".strip()
