from _dependencies.exceptions import DependencyError
from _dependencies.graph import _Graph
from _dependencies.objects.nested import _InjectorTypeType
from _dependencies.resolve import _Resolver
from _dependencies.state import _State


class _InjectorType(_InjectorTypeType):
    def __new__(cls, class_name, bases, namespace):
        if not bases:
            namespace["__dependencies__"] = _Graph()
            # Doctest module compatibility.
            namespace["__wrapped__"] = None  # pragma: no mutate
            # Typing module compatibility.
            namespace["_subs_tree"] = None  # pragma: no mutate
            return type.__new__(cls, class_name, bases, namespace)

        _check_inheritance(bases, Injector)
        ns = {}
        for attr in ("__module__", "__doc__", "__weakref__", "__qualname__"):
            _transfer(namespace, ns, attr)
        _check_extension_scope(bases, namespace)
        dependencies = _Graph()
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies.assign(name, dep)
        ns["__dependencies__"] = dependencies
        return type.__new__(cls, class_name, bases, ns)

    def __call__(cls, **kwargs):
        """Produce new Injector with some dependencies overwritten."""
        return type(cls.__name__, (cls,), kwargs)

    def __getattr__(cls, attrname):
        __tracebackhide__ = True
        return _Resolver(cls, _State(cls, attrname)).resolve(attrname)

    def __setattr__(cls, attrname, value):
        raise DependencyError("'Injector' modification is not allowed")

    def __delattr__(cls, attrname):
        raise DependencyError("'Injector' modification is not allowed")

    def __contains__(cls, attrname):
        return cls.__dependencies__.has(attrname)

    def __and__(cls, other):
        return type(cls.__name__, (cls, other), {})

    def __dir__(cls):
        parent = set(dir(cls.__base__))
        current = set(cls.__dict__) - {"__dependencies__", "__wrapped__", "_subs_tree"}
        dependencies = set(cls.__dependencies__.specs) - {"__parent__"}
        attributes = sorted(parent | current | dependencies)
        return attributes


def _transfer(from_namespace, to_namespace, attr):
    try:
        to_namespace[attr] = from_namespace.pop(attr)
    except KeyError:
        pass


def _check_inheritance(bases, injector):
    for base in bases:
        if not issubclass(base, injector):
            message = "Multiple inheritance is allowed for Injector subclasses only"
            raise DependencyError(message)


def _check_extension_scope(bases, namespace):
    if len(bases) == 1 and not namespace:
        raise DependencyError("Extension scope can not be empty")


class Injector(metaclass=_InjectorType):
    """Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into classes specified in
    it namespace.

    """
