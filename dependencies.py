"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import inspect

import six

__all__ = ['Injector', 'DependencyError']


class InjectorType(type):

    def __new__(cls, name, bases, namespace):

        if len(bases) == 0:
            namespace['__dependencies__'] = {}
            return type.__new__(cls, name, bases, namespace)

        if len(bases) > 1:
            raise DependencyError(
                'Multiple inheritance is not allowed')

        ns = {}

        for attr in ('__module__', '__doc__', '__weakref__', '__qualname__'):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass

        if any(dunder_name(x) for x in namespace):
            raise DependencyError('Magic methods are not allowed')

        if 'let' in namespace:
            raise DependencyError("'let' redefinition is not allowed")

        dependencies = {}
        dependencies.update(bases[0].__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = make_dependency_spec(name, dep)
        check_circles(dependencies)
        ns['__dependencies__'] = dependencies

        return type.__new__(cls, name, bases, ns)

    def __getattr__(cls, attrname):

        try:
            attribute_spec = cls.__dependencies__[attrname]
        except KeyError:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'
                .format(cls.__name__, attrname))
        attribute, argspec = attribute_spec
        if argspec is None:
            return attribute
        if argspec is False:
            return attribute()
        args, have_defaults = argspec
        arguments = []
        keywords = {}
        for n, a in enumerate(args, 1):
            try:
                arguments.append(getattr(cls, a))
            except AttributeError:
                if n < have_defaults:
                    raise
        return attribute(*arguments, **keywords)

    def __setattr__(cls, attrname, value):

        if cls.__bases__ == (object,):
            raise DependencyError("'Injector' modification is not allowed")
        if dunder_name(attrname):
            raise DependencyError('Magic methods are not allowed')
        if attrname == 'let':
            raise DependencyError("'let' redefinition is not allowed")
        cls.__dependencies__[attrname] = make_dependency_spec(attrname, value)

    def __delattr__(cls, attrname):

        if attrname not in cls.__dependencies__:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'
                .format(cls.__name__, attrname))
        del cls.__dependencies__[attrname]

    def __dir__(cls):

        parent = set(dir(cls.__base__))
        current = set(cls.__dict__.keys()) - set(['__dependencies__'])
        dependencies = set(cls.__dependencies__.keys())
        attributes = sorted(parent | current | dependencies)
        return attributes


class Injector(six.with_metaclass(InjectorType)):
    """
    Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into
    classes specified in it namespace.
    """

    def __init__(self, *args, **kwargs):

        raise DependencyError('Do not instantiate Injector')

    @classmethod
    def let(cls, **kwargs):
        """Produce new Injector with some dependencies overwritten."""

        return type(cls.__name__, (cls,), kwargs)


class DependencyError(Exception):
    """Broken dependencies configuration error."""

    pass


def make_dependency_spec(name, dependency):
    """Make spec to store dependency in the __dependencies__."""

    if inspect.isclass(dependency) and not name.endswith('_cls'):
        if use_object_init(dependency):
            return dependency, False
        else:
            argspec = inspect.getargspec(dependency.__init__)
            args, varargs, kwargs, defaults = argspec
            check_varargs(dependency, varargs, kwargs)
            if defaults is not None:
                have_defaults = len(args) - len(defaults)
            else:
                have_defaults = len(args)
            spec = args[1:], have_defaults
            return dependency, spec
    else:
        return dependency, None


def use_object_init(cls):
    """Check if cls.__init__ will get us object.__init__."""

    if '__init__' in cls.__dict__:
        return False
    else:
        if cls.__bases__ == (object,):
            return True
        else:
            for base in cls.__bases__:
                if not use_object_init(base):
                    return False
            else:
                return True


def dunder_name(name):
    """Check if name is dunder method name."""

    return name.startswith('__') and name.endswith('__')


def check_varargs(dependency, varargs, kwargs):
    """Deny *args and **kwargs in the dependency constructor with proper message."""

    if varargs and kwargs:
        raise DependencyError(
            '{0!r}.__init__ have arbitrary argument list and keyword arguments'
            .format(dependency)
        )
    elif varargs:
        raise DependencyError(
            '{0!r}.__init__ have arbitrary argument list'
            .format(dependency)
        )
    elif kwargs:
        raise DependencyError(
            '{0!r}.__init__ have arbitrary keyword arguments'
            .format(dependency)
        )


def check_circles(dependencies):
    """Check if dependencies has circles in argument names."""

    for depname in dependencies:
        check_circles_for(dependencies, depname, depname)


def check_circles_for(dependencies, attrname, origin):
    """Check circle for one dependency."""

    try:
        attribute_spec = dependencies[attrname]
    except KeyError:
        return
    attribute, argspec = attribute_spec
    if argspec:
        args = argspec[0]
        if origin in args:
            raise DependencyError(
                '{0!r} is a circle dependency in the {1!r} constructor'
                .format(origin, attribute)
            )
        for name in args:
            check_circles_for(dependencies, name, origin)
