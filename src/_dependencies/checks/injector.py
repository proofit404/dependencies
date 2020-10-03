from inspect import isdatadescriptor
from inspect import ismethoddescriptor

from _dependencies.exceptions import DependencyError


def _check_inheritance(bases, injector):

    for base in bases:
        if not issubclass(base, injector):
            message = "Multiple inheritance is allowed for Injector subclasses only"
            raise DependencyError(message)


def _check_extension_scope(bases, namespace):
    if len(bases) == 1 and not namespace:
        raise DependencyError("Extension scope can not be empty")


def _check_dunder_name(name):

    if name.startswith("__") and name.endswith("__"):
        raise DependencyError("Magic methods are not allowed")


def _check_descriptor(class_name, name, dependency):
    if ismethoddescriptor(dependency) or isdatadescriptor(dependency):
        message = descriptor_template.format(class_name=class_name, name=name)
        raise DependencyError(message)


# Messages.


descriptor_template = """
'{class_name}.{name}' contains descriptor.

Descriptors usage will be confusing inside Injector subclasses.

Use @value decorator instead, if you really need inject descriptor instance somewhere.
""".strip()
