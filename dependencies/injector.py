"""
dependencies.injector
~~~~~~~~~~~~~~~~~~~~~

This module implements Injector class (general DI mechanism).

:copyright: (c) 2016-2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

import inspect
import weakref

from .exceptions import DependencyError
from .proxies import ProxyType, Thisable


class InjectorType(type):

    def __new__(cls, class_name, bases, namespace):

        if not bases:
            namespace['__dependencies__'] = {}
            return type.__new__(cls, class_name, bases, namespace)
        check_inheritance(bases)
        ns = {}
        for attr in ('__module__', '__doc__', '__weakref__', '__qualname__'):
            try:
                ns[attr] = namespace.pop(attr)
            except KeyError:
                pass
        for k, v in namespace.items():
            check_dunder_name(k)
            check_attrs_redefinition(k)
            check_proxies(v)
        dependencies = {}
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = make_dependency_spec(name, dep)
        check_loops(class_name, dependencies)
        check_circles(dependencies)
        ns['__dependencies__'] = dependencies
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
                if current_attr == '__parent__':
                    raise DependencyError('You tries to shift this more times '
                                          'that Injector has levels')
                else:
                    raise AttributeError('{0!r} object has no attribute {1!r}'
                                         .format(cls.__name__, current_attr))
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
                subclass.__dependencies__['__parent__'] = parent_spec
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

    def __and__(cls, other):

        return type(cls.__name__, (cls, other), {})

    def __dir__(cls):

        parent = set(dir(cls.__base__))
        current = set(cls.__dict__) - set(['__dependencies__'])
        dependencies = set(cls.__dependencies__) - set(['__parent__'])
        attributes = sorted(parent | current | dependencies)
        return attributes


def __init__(self, *args, **kwargs):

    raise DependencyError('Do not instantiate Injector')


@classmethod
def let(cls, **kwargs):
    """Produce new Injector with some dependencies overwritten."""

    return type(cls.__name__, (cls,), kwargs)


injector_doc = """
Default dependencies specification DSL.

Classes inherited from this class may inject dependencies into classes
specified in it namespace.
"""

Injector = InjectorType('Injector', (), {
    '__init__': __init__,
    '__doc__': injector_doc,
    'let': let,
})


class Marker(object):

    def __bool__(self):

        return False

    __nonzero__ = __bool__


nested_injector = Marker()


def make_dependency_spec(name, dependency):

    if inspect.isclass(dependency) and \
       not name.endswith('_cls'):
        if issubclass(dependency, Injector):
            return dependency, nested_injector
        elif use_object_init(dependency):
            return dependency, False
        else:
            spec = make_init_spec(dependency)
            return dependency, spec
    else:
        return dependency, None


try:
    inspect.signature
except AttributeError:

    def make_init_spec(dependency):

        argspec = inspect.getargspec(dependency.__init__)
        args, varargs, kwargs, defaults = argspec
        check_varargs(dependency, varargs, kwargs)
        if defaults is not None:
            check_cls_arguments(args, defaults)
            have_defaults = len(args) - len(defaults)
        else:
            have_defaults = len(args)
        spec = args[1:], have_defaults
        return spec
else:

    def make_init_spec(dependency):

        signature = inspect.signature(dependency.__init__)
        parameters = iter(signature.parameters.items())
        next(parameters)
        args, defaults = [], []
        varargs = kwargs = None
        have_defaults = 1
        for name, param in parameters:
            args.append(name)
            if param.default is not param.empty:
                defaults.append(param.default)
            else:
                have_defaults += 1
            if param.kind is param.VAR_POSITIONAL:
                varargs = True
            if param.kind is param.VAR_KEYWORD:
                kwargs = True
        check_varargs(dependency, varargs, kwargs)
        if defaults:
            check_cls_arguments(args, defaults)
        return args, have_defaults


def use_object_init(cls):

    for base in cls.__mro__:
        if base is object:
            return True
        elif '__init__' in base.__dict__:
            return False


def check_inheritance(bases):

    for base in bases:
        if not issubclass(base, Injector):
            raise DependencyError(
                'Multiple inheritance is allowed for Injector subclasses only',
            )


def check_dunder_name(name):

    if name.startswith('__') and name.endswith('__'):
        raise DependencyError('Magic methods are not allowed')


def check_attrs_redefinition(name):

    if name == 'let':
        raise DependencyError("'let' redefinition is not allowed")


def check_cls_arguments(argnames, defaults):

    for name, value in zip(reversed(argnames), reversed(defaults)):
        expect_class = name.endswith('_cls')
        is_class = inspect.isclass(value)
        if expect_class and not is_class:
            raise DependencyError(
                '{0!r} default value should be a class'.format(name),
            )
        if not expect_class and is_class:
            raise DependencyError(
                "{0!r} argument can not have class as its default value"
                .format(name),
            )


def check_varargs(dependency, varargs, kwargs):

    if varargs and kwargs:
        message = ('{0}.__init__ have arbitrary argument list '
                   'and keyword arguments')
        raise DependencyError(message.format(dependency.__name__))
    elif varargs:
        message = '{0}.__init__ have arbitrary argument list'
        raise DependencyError(message.format(dependency.__name__))
    elif kwargs:
        message = '{0}.__init__ have arbitrary keyword arguments'
        raise DependencyError(message.format(dependency.__name__))


def check_loops(class_name, dependencies):

    for argument_name, (dep, depspec) in dependencies.items():
        if isinstance(dep, ProxyType):
            check_loops_for(
                class_name,
                argument_name,
                dependencies,
                dep,
                filter_expression(dep),
            )
        elif depspec is nested_injector:
            nested_dependencies = {'__parent__': (dependencies, None)}
            nested_dependencies.update(dep.__dependencies__)
            check_loops(class_name, nested_dependencies)


def check_loops_for(class_name, argument_name, dependencies, origin,
                    expression):

    try:
        argname = next(expression)
    except StopIteration:
        return
    try:
        attribute, argspec = dependencies[argname]
    except KeyError:
        return
    if argspec is nested_injector:
        nested_dependencies = {'__parent__': (dependencies, None)}
        nested_dependencies.update(attribute.__dependencies__)
        check_loops_for(
            class_name,
            argument_name,
            nested_dependencies,
            origin,
            expression,
        )
    elif argname == '__parent__':
        check_loops_for(
            class_name,
            argument_name,
            attribute,
            origin,
            expression,
        )
    elif attribute is origin:
        raise DependencyError(
            '{0!r} is a circle link in the {1!r} injector'.format(
                argument_name,
                class_name,
            ),
        )
    elif isinstance(attribute, ProxyType):
        check_loops_for(
            class_name,
            argument_name,
            dependencies,
            origin,
            filter_expression(attribute),
        )


def filter_expression(proxy):

    for parent in range(proxy.__parents__):
        yield '__parent__'
    for symbol in proxy.__expression__:
        if symbol == '.':
            continue
        elif symbol == '[':
            raise StopIteration()
        else:
            yield symbol


def check_circles(dependencies):

    for depname in dependencies:
        check_circles_for(dependencies, depname, depname)


def check_circles_for(dependencies, attrname, origin):

    try:
        attribute_spec = dependencies[attrname]
    except KeyError:
        return
    attribute, argspec = attribute_spec
    if argspec:
        args = argspec[0]
        if origin in args:
            message = '{0!r} is a circle dependency in the {1!r} constructor'
            raise DependencyError(message.format(origin, attribute.__name__))
        for name in args:
            check_circles_for(dependencies, name, origin)


def check_proxies(dependency):

    if isinstance(dependency, Thisable):
        raise DependencyError(
            "You can not use 'this' directly in the 'Injector'",
        )
