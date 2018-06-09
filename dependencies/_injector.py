import inspect
import weakref

from ._checks.circles import check_circles
from ._checks.links import check_links
from ._spec import make_init_spec, nested_injector, use_object_init
from ._this import Thisable
from .exceptions import DependencyError


class InjectorType(type):

    def __new__(cls, class_name, bases, namespace):

        if not bases:
            namespace["__dependencies__"] = {}
            return type.__new__(cls, class_name, bases, namespace)

        check_inheritance(bases)
        ns = {}
        for attr in ("__module__", "__doc__", "__weakref__", "__qualname__"):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass
        for k, v in namespace.items():
            check_dunder_name(k)
            check_attrs_redefinition(k)
            check_thisable(v)
        dependencies = {}
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = make_dependency_spec(name, dep)
        check_links(class_name, dependencies)
        check_circles(dependencies)
        ns["__dependencies__"] = dependencies
        return type.__new__(cls, class_name, bases, ns)

    def __getattr__(cls, attrname):

        cache, cached = {}, set()
        current_attr, attrs_stack = attrname, [attrname]
        have_default = False
        while attrname not in cache:
            attribute_spec = cls.__dependencies__.get(current_attr)
            if attribute_spec is None:
                if have_default:
                    cached.add(current_attr)
                    current_attr = attrs_stack.pop()
                    have_default = False
                    continue

                if current_attr == "__parent__":
                    raise DependencyError(
                        "You tries to shift this more times that Injector has levels"
                    )
                else:
                    if len(attrs_stack) > 1:
                        message = "{0!r} can not resolve attribute {1!r} while building {2!r}".format(
                            cls.__name__, current_attr, attrs_stack.pop()
                        )
                    else:
                        message = "{0!r} can not resolve attribute {1!r}".format(
                            cls.__name__, current_attr
                        )
                    raise DependencyError(message)

            attribute, argspec = attribute_spec
            if argspec is None:
                cache[current_attr] = attribute
                cached.add(current_attr)
                current_attr = attrs_stack.pop()
                have_default = False
                continue

            if argspec is False:
                cache[current_attr] = attribute()
                cached.add(current_attr)
                current_attr = attrs_stack.pop()
                have_default = False
                continue

            if argspec is nested_injector:
                subclass = type(attribute.__name__, (attribute,), {})
                parent_spec = weakref.ref(cls), False
                subclass.__dependencies__["__parent__"] = parent_spec
                cache[current_attr] = subclass
                cached.add(current_attr)
                current_attr = attrs_stack.pop()
                have_default = False
                continue

            args, have_defaults = argspec
            if set(args).issubset(cached):
                kwargs = dict((k, cache[k]) for k in args if k in cache)
                cache[current_attr] = attribute(**kwargs)
                cached.add(current_attr)
                current_attr = attrs_stack.pop()
                have_default = False
                continue

            for n, arg in enumerate(args, 1):
                if arg not in cached:
                    attrs_stack.append(current_attr)
                    current_attr = arg
                    have_default = False if n < have_defaults else True
                    break

        return cache[attrname]

    def __setattr__(cls, attrname, value):

        raise DependencyError("'Injector' modification is not allowed")

    def __delattr__(cls, attrname):

        raise DependencyError("'Injector' modification is not allowed")

    def __contains__(cls, attrname):

        return attrname in cls.__dependencies__

    def __and__(cls, other):

        return type(cls.__name__, (cls, other), {})

    def __dir__(cls):

        parent = set(dir(cls.__base__))
        current = set(cls.__dict__) - set(["__dependencies__"])
        dependencies = set(cls.__dependencies__) - set(["__parent__"])
        attributes = sorted(parent | current | dependencies)
        return attributes


def __init__(self, *args, **kwargs):

    raise DependencyError("Do not instantiate Injector")


@classmethod
def let(cls, **kwargs):
    """Produce new Injector with some dependencies overwritten."""

    return type(cls.__name__, (cls,), kwargs)


injector_doc = """
Default dependencies specification DSL.

Classes inherited from this class may inject dependencies into classes
specified in it namespace.
"""

Injector = InjectorType(
    "Injector", (), {"__init__": __init__, "__doc__": injector_doc, "let": let}
)


def make_dependency_spec(name, dependency):

    if inspect.isclass(dependency) and not name.endswith("_class"):
        if issubclass(dependency, Injector):
            return dependency, nested_injector

        elif use_object_init(dependency):
            return dependency, False

        else:
            spec = make_init_spec(dependency)
            return dependency, spec

    else:
        return dependency, None


def check_inheritance(bases):

    for base in bases:
        if not issubclass(base, Injector):
            raise DependencyError(
                "Multiple inheritance is allowed for Injector subclasses only"
            )


def check_dunder_name(name):

    if name.startswith("__") and name.endswith("__"):
        raise DependencyError("Magic methods are not allowed")


def check_attrs_redefinition(name):

    if name == "let":
        raise DependencyError("'let' redefinition is not allowed")


def check_thisable(dependency):

    if isinstance(dependency, Thisable):
        raise DependencyError("You can not use 'this' directly in the 'Injector'")
