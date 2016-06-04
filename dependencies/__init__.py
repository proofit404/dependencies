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

        if any(x for x in namespace
               if x.startswith('__') and x.endswith('__')):
            raise DependencyError('Magic methods are not allowed')

        if 'let' in namespace:
            raise DependencyError("'let' redefinition is not allowed")

        dependencies = {}
        dependencies.update(bases[0].__dependencies__)
        dependencies.update(namespace)
        check_circles(dependencies)
        ns['__dependencies__'] = dependencies

        return type.__new__(cls, name, bases, ns)

    def __getattr__(cls, attrname):

        try:
            attribute = cls.__dependencies__[attrname]
        except KeyError:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'
                .format(cls.__name__, attrname))
        if inspect.isclass(attribute) and not attrname.endswith('_cls'):
            if use_object_init(attribute):
                return attribute()
            init = attribute.__init__
            args, varargs, kwargs, defaults = inspect.getargspec(init)
            if defaults is not None:
                have_defaults = len(args) - len(defaults)
            else:
                have_defaults = len(args)
            arguments = []
            keywords = {}
            for n, a in enumerate(args[1:], 1):
                try:
                    arguments.append(getattr(cls, a))
                except AttributeError:
                    if n < have_defaults:
                        raise
                    else:
                        arguments.append(defaults[n - have_defaults])
            if varargs is not None:
                arguments.extend(getattr(cls, varargs))
            if kwargs is not None:
                keywords.update(getattr(cls, kwargs))
            return attribute(*arguments, **keywords)
        else:
            return attribute

    def __dir__(cls):

        parent = set(dir(cls.__base__))
        current = set(cls.__dict__.keys()) - set(['__dependencies__'])
        dependencies = set(cls.__dependencies__.keys())
        attributes = sorted(parent | current | dependencies)
        return attributes


class Injector(six.with_metaclass(InjectorType)):
    """Default dependencies specification DSL.

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


def check_circles(dependencies):
    """Check if dependencies has circles in argument names."""

    for depname in dependencies:
        check_circles_for(dependencies, depname, depname)


def check_circles_for(dependencies, attrname, origin):
    """Check circle for one dependency."""

    try:
        attribute = dependencies[attrname]
    except KeyError:
        return
    if inspect.isclass(attribute) and not use_object_init(attribute):
        args, varargs, kwargs, _ = inspect.getargspec(attribute.__init__)
        names = [name for name in args[1:] + [varargs, kwargs] if name]
        if origin in names:
            raise DependencyError(
                '{0!r} is a circle dependency in the {1!r} constructor'
                .format(origin, attribute))
        for name in names:
            check_circles_for(dependencies, name, origin)
