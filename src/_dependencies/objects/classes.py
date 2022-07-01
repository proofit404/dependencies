from inspect import isclass

from _dependencies.exceptions import DependencyError
from _dependencies.injectable import _method_args
from _dependencies.scope import _IsScope
from _dependencies.spec import _Spec


def _is_class(name, dependency):
    return isclass(dependency) and not name.endswith("_class")


def _build_class_spec(name, dependency):
    if _using_object_init(dependency):
        return _Spec(_ClassFactory(dependency), {}, set(), set(), lambda: None, False)
    else:
        name = dependency.__name__ + "." + "__init__"
        owner = f"{dependency.__name__!r} class"
        args, required, optional = _method_args(dependency.__init__, name, owner)
        return _Spec(
            _ClassFactory(dependency), args, required, optional, lambda: None, False
        )


def _using_object_init(cls):
    for base in cls.__mro__:  # pragma: no branch
        if base is object:
            return True
        elif "__init__" in base.__dict__:
            return False


class _ClassFactory:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, **kwargs):
        message = no_depend_nested_injector_template
        for argument in kwargs.values():
            if isinstance(argument, _IsScope):
                raise DependencyError(message)
        return self.cls(**kwargs), None


# Messages.


no_depend_nested_injector_template = """
Do not depend on nested injectors directly.

Use this object to access inner attributes of nested injector
""".strip()
