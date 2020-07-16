# -*- coding: utf-8 -*-
from _dependencies.attributes import _Replace
from _dependencies.checks.circles import _check_circles
from _dependencies.checks.injector import _check_attrs_redefinition
from _dependencies.checks.injector import _check_dunder_name
from _dependencies.checks.injector import _check_inheritance
from _dependencies.checks.loops import _check_loops
from _dependencies.exceptions import DependencyError
from _dependencies.replace import _deep_replace_dependency
from _dependencies.spec import _InjectorTypeType
from _dependencies.spec import _make_dependency_spec


class _InjectorType(_InjectorTypeType):
    def __new__(cls, class_name, bases, namespace):

        if not bases:
            namespace["__dependencies__"] = {}
            namespace["__wrapped__"] = None  # Doctest module compatibility.
            namespace["_subs_tree"] = None  # Typing module compatibility.
            return type.__new__(cls, class_name, bases, namespace)

        _check_inheritance(bases, Injector)
        ns = {}
        for attr in ("__module__", "__doc__", "__weakref__", "__qualname__"):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass
        for name in namespace:
            _check_dunder_name(name)
            _check_attrs_redefinition(name)
        dependencies = {}
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = _make_dependency_spec(name, dep)
        _check_loops(class_name, dependencies)
        _check_circles(dependencies)
        ns["__dependencies__"] = dependencies
        return type.__new__(cls, class_name, bases, ns)

    def __getattr__(cls, attrname):
        __tracebackhide__ = True

        cache, cached = {"__self__": cls}, {"__self__"}
        current_attr, attrs_stack = attrname, [attrname]
        have_default = False

        while attrname not in cache:

            spec = cls.__dependencies__.get(current_attr)

            if spec is None:
                if have_default:
                    cached.add(current_attr)
                    current_attr = attrs_stack.pop()
                    have_default = False
                    continue
                if len(attrs_stack) > 1:
                    message = "{!r} can not resolve attribute {!r} while building {!r}".format(  # noqa: E501
                        cls.__name__, current_attr, attrs_stack.pop()
                    )
                else:
                    message = "{!r} can not resolve attribute {!r}".format(
                        cls.__name__, current_attr
                    )
                raise DependencyError(message)

            marker, attribute, args, have_defaults = spec

            if set(args).issubset(cached):
                kwargs = {k: cache[k] for k in args if k in cache}

                try:
                    cache[current_attr] = attribute(**kwargs)
                except _Replace as replace:
                    _deep_replace_dependency(cls, current_attr, replace)
                    _check_loops(cls.__name__, cls.__dependencies__)
                    _check_circles(cls.__dependencies__)
                    continue

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
        current = set(cls.__dict__) - {"__dependencies__", "__wrapped__", "_subs_tree"}
        dependencies = set(cls.__dependencies__) - {"__parent__"}
        attributes = sorted(parent | current | dependencies)
        return attributes


def __init__(self, *args, **kwargs):

    raise DependencyError("Do not instantiate Injector")


def let(cls, **kwargs):
    """Produce new Injector with some dependencies overwritten."""
    return type(cls.__name__, (cls,), kwargs)


injector_doc = """
Default dependencies specification DSL.

Classes inherited from this class may inject dependencies into classes
specified in it namespace.
"""


Injector = _InjectorType(
    "Injector",
    (),
    {"__init__": __init__, "__doc__": injector_doc, "let": classmethod(let)},
)
