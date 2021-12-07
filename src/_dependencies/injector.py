from _dependencies.exceptions import DependencyError
from _dependencies.graph import _Graph
from _dependencies.lazy import _LazyGraph
from _dependencies.objects.nested import _InjectorTypeType
from _dependencies.scope import _Scope


class _InjectorType(_InjectorTypeType):
    def __new__(cls, class_name, bases, namespace):
        if not bases:
            namespace["__dependencies__"] = _Graph()
            # Doctest module compatibility.
            namespace["__wrapped__"] = None  # pragma: no mutate
            # Typing module compatibility.
            namespace["_subs_tree"] = None  # pragma: no mutate
            return type.__new__(cls, class_name, bases, namespace)
        else:
            ns = {}
            _transfer(namespace, ns)
            _check_inheritance(bases)
            _check_extension_scope(bases, namespace)
            ns["__dependencies__"] = _LazyGraph("__dependencies__", namespace)
            return type.__new__(cls, class_name, bases, ns)

    def __call__(cls, **kwargs):
        return type(cls.__name__, (cls,), kwargs)

    def __and__(cls, other):
        return type(cls.__name__, (cls, other), {})

    def __enter__(cls):
        return _Scope(cls.__name__, cls.__dependencies__)

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __getattr__(cls, attrname):
        scope = _Scope(cls.__name__, cls.__dependencies__)
        resolved = getattr(scope, attrname)
        cls.__dependencies__.get(attrname).resolved()
        return resolved

    def __setattr__(cls, attrname, value):
        raise DependencyError("'Injector' modification is not allowed")

    def __delattr__(cls, attrname):
        raise DependencyError("'Injector' modification is not allowed")

    def __contains__(cls, attrname):
        return cls.__dependencies__.has(attrname)

    def __dir__(cls):
        return sorted(cls.__dependencies__.specs)


def _transfer(from_namespace, to_namespace):
    for attr in ("__module__", "__doc__", "__weakref__", "__qualname__"):
        try:
            to_namespace[attr] = from_namespace.pop(attr)
        except KeyError:
            pass


def _check_inheritance(bases):
    for base in bases:
        if not issubclass(base, Injector):
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
