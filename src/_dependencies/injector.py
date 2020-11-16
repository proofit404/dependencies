from collections import deque

from _dependencies.attributes import _Replace
from _dependencies.checks.circles import _check_circles
from _dependencies.checks.injector import _check_dunder_name
from _dependencies.checks.injector import _check_extension_scope
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
        _check_extension_scope(bases, namespace)
        for name in namespace:
            _check_dunder_name(name)
        dependencies = {}
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = _make_dependency_spec(name, dep)
        _check_loops(class_name, dependencies)
        _check_circles(dependencies)
        ns["__dependencies__"] = dependencies
        return type.__new__(cls, class_name, bases, ns)

    def __call__(cls, **kwargs):
        """Produce new Injector with some dependencies overwritten."""
        return type(cls.__name__, (cls,), kwargs)

    def __getattr__(cls, attrname):
        __tracebackhide__ = True

        state = _State(cls, attrname)

        while attrname not in state.cache:

            spec = cls.__dependencies__.get(state.current)

            if spec is None:
                if state.have_default:
                    state.pop()
                    continue
                if state.full():
                    message = "{!r} can not resolve attribute {!r} while building {!r}".format(  # noqa: E501
                        cls.__name__, state.current, state.stack.pop()[0]
                    )
                else:
                    message = "{!r} can not resolve attribute {!r}".format(
                        cls.__name__, state.current
                    )
                raise DependencyError(message)

            marker, attribute, args, required, optional = spec

            if state.resolved(required, optional):
                try:
                    state.store(attribute(**state.kwargs(args)))
                except _Replace as replace:
                    _deep_replace_dependency(cls, state.current, replace)
                    _check_loops(cls.__name__, cls.__dependencies__)
                    _check_circles(cls.__dependencies__)
                continue

            for arg, default in args.items():
                if state.should(arg, default):
                    state.add(arg, default)
                    break

        return state.cache[attrname]

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


class _State:
    def __init__(self, injector, attrname):
        self.cache = {"__self__": injector}
        self.tried = set()
        self.stack = deque()
        self.current = attrname
        self.have_default = False

    def add(self, current, have_default):
        self.stack.append((self.current, self.have_default))
        self.current = current
        self.have_default = have_default

    def pop(self):
        self.tried.add(self.current)
        try:
            self.current, self.have_default = self.stack.pop()
        except IndexError:
            pass

    def store(self, value):
        self.cache[self.current] = value
        self.pop()

    def resolved(self, required, optional):
        has_required = required <= self.cache.keys()
        tried_optional = optional <= self.tried
        return has_required and tried_optional

    def kwargs(self, args):
        return {k: self.cache[k] for k in args if k in self.cache}

    def should(self, arg, have_default):
        return arg not in self.tried or (arg not in self.cache and not have_default)

    def full(self):
        return len(self.stack) > 0


class Injector(metaclass=_InjectorType):
    """Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into classes specified in
    it namespace.

    """
