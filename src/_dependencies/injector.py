from _dependencies.delegate import _Delegate
from _dependencies.exceptions import DependencyError
from _dependencies.graph import _Graph
from _dependencies.lazy import _LazyGraph
from _dependencies.objects.nested import _InjectorTypeType
from _dependencies.scope import _Scope
from _dependencies.stack import _Stack


class _InjectorType(_InjectorTypeType):
    def __new__(cls, class_name, bases, namespace):
        if not bases:
            namespace["__dependencies__"] = _Graph()
            namespace["__context_stack__"] = _Stack()
            # Doctest module compatibility.
            namespace["__wrapped__"] = None  # pragma: no mutate
            return type.__new__(cls, class_name, bases, namespace)
        else:
            ns = {}
            _transfer(namespace, ns)
            _check_inheritance(bases)
            _check_extension_scope(bases, namespace)
            ns["__dependencies__"] = _LazyGraph("__dependencies__", namespace)
            ns["__context_stack__"] = _Stack()
            return type.__new__(cls, class_name, bases, ns)

    def __call__(cls, **kwargs):
        return type(cls.__name__, (cls,), kwargs)

    def __and__(cls, other):
        return type(cls.__name__, (cls, other), {})

    def __enter__(cls):
        enclose = cls.__context_stack__.add()
        scope = _Scope(cls.__name__, cls.__dependencies__, enclose.before)
        return _Delegate(cls.__name__, cls.__dependencies__, scope)

    def __exit__(cls, exc_type, exc_value, traceback):
        cls.__context_stack__.remove()

    def __getattr__(cls, attrname):
        scope = _Scope(cls.__name__, cls.__dependencies__, lambda graph, cache: None)
        delegate = _Delegate(cls.__name__, cls.__dependencies__, scope)
        return getattr(delegate, attrname)

    def __setattr__(cls, attrname, value):
        raise DependencyError("'Injector' modification is not allowed")

    def __delattr__(cls, attrname):
        raise DependencyError("'Injector' modification is not allowed")

    def __contains__(cls, attrname):
        return cls.__dependencies__.has(attrname)

    def __dir__(cls):
        return sorted(cls.__dependencies__.specs)


def _transfer(source, destination):
    for attr in ("__module__", "__doc__", "__weakref__", "__qualname__"):
        if attr in source:
            destination[attr] = source.pop(attr)


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
