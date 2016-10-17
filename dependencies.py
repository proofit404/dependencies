"""
    dependencies
    ~~~~~~~~~~~~

    Dependency Injection for Humans.

    :copyright: (c) 2016 by Artem Malyshev.
    :license: LGPL-3, see LICENSE for more details.
"""

import inspect
import weakref


__all__ = ['Injector', 'attribute', 'item', 'DependencyError']


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
        for x in namespace:
            check_dunder_name(x)
            check_attrs_redefinition(x)
        dependencies = {}
        for base in reversed(bases):
            dependencies.update(base.__dependencies__)
        for name, dep in namespace.items():
            dependencies[name] = make_dependency_spec(name, dep)
        check_circles(dependencies)
        ns['__dependencies__'] = dependencies
        result = type.__new__(cls, class_name, bases, ns)
        for dep in namespace.values():
            maybe_insert_parent(result, dep)
        return result

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
                raise AttributeError(
                    '{0!r} object has no attribute {1!r}'
                    .format(cls.__name__, current_attr)
                )
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
            else:
                current_attr = attrs_stack.pop()
                have_default = False
        return cache[attrname]

    def __setattr__(cls, attrname, value):

        if cls.__bases__ == (object,):
            raise DependencyError("'Injector' modification is not allowed")
        check_dunder_name(attrname)
        check_attrs_redefinition(attrname)
        cls.__dependencies__[attrname] = make_dependency_spec(attrname, value)
        check_circles(cls.__dependencies__)
        maybe_insert_parent(cls, value)

    def __delattr__(cls, attrname):

        check_dunder_name(attrname)
        check_attrs_redefinition(attrname)
        if attrname not in cls.__dependencies__:
            raise AttributeError(
                '{0!r} object has no attribute {1!r}'
                .format(cls.__name__, attrname)
            )
        del cls.__dependencies__[attrname]

    def __and__(cls, other):

        return type(cls.__name__, (cls, other), {})

    def __dir__(cls):

        parent = set(dir(cls.__base__))
        current = set(cls.__dict__) - set(['__dependencies__'])
        dependencies = set(cls.__dependencies__)
        attributes = sorted(parent | current | dependencies)
        return attributes


def __init__(self, *args, **kwargs):

    raise DependencyError('Do not instantiate Injector')


@classmethod
def let(cls, **kwargs):
    """Produce new Injector with some dependencies overwritten."""

    return type(cls.__name__, (cls,), kwargs)


use_doc = """
Decorator based injector modification.

Similar to attribute assignment.
"""


class Use(object):

    def __get__(self, obj, objtype):

        class Register(object):

            def __getattribute__(self, attrname):

                if attrname == '__doc__':
                    return use_doc

                def register(dependency):

                    check_dunder_name(attrname)
                    check_attrs_redefinition(attrname)
                    spec = make_dependency_spec(attrname, dependency)
                    objtype.__dependencies__[attrname] = spec
                    check_circles(objtype.__dependencies__)
                    maybe_insert_parent(objtype, dependency)
                    return dependency

                return register

        return Register()


Injector = InjectorType('Injector', (), {
    '__init__': __init__,
    'let': let,
    'use': Use(),
    '__doc__': """
    Default dependencies specification DSL.

    Classes inherited from this class may inject dependencies into
    classes specified in it namespace.
    """,
})


class DependencyError(Exception):
    """Broken dependencies configuration error."""

    pass


def attribute(target, *attrs):
    """TODO: write *and* test doc."""

    target = '__parent__' if target == '..' else target
    check_empty('attrs', attrs)
    __new__ = attrgetter(target, attrs)
    __init__ = make_init(target)
    return type('Attribute', (object,), {
        '__new__': __new__,
        '__init__': __init__,
    })


def item(target, *items):
    """TODO: write *and* test doc."""

    check_empty('items', items)
    __new__ = itemgetter(target, items)
    __init__ = make_init(target)
    return type('Item', (object,), {
        '__new__': __new__,
        '__init__': __init__,
    })


def make_dependency_spec(name, dependency):

    if inspect.isclass(dependency) and \
       not name.endswith('_cls') and   \
       not issubclass(dependency, Injector):
        if use_object_init(dependency):
            return dependency, False
        else:
            spec = make_init_spec(dependency)
            return dependency, spec
    else:
        return dependency, None


def maybe_insert_parent(parent, dependency):
    """Make weak reference between Injector and nested Injector."""

    if inspect.isclass(dependency) and issubclass(dependency, Injector):
        spec = (weakref.ref(parent), False)
        dependency.__dependencies__['__parent__'] = spec


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


def attrgetter(argument, attrs):

    def new(cls, target):
        result = target
        for attr in attrs:
            result = getattr(result, attr)
        return result

    getter = make_new(argument, new)
    return getter


def itemgetter(argument, items):

    def new(cls, target):
        result = target
        for item in items:
            result = result[item]
        return result

    getter = make_new(argument, new)
    return getter


def make_new(argument, callback):

    template = 'def __new__(cls, {argument}): return callback(cls, {argument})'
    code = template.format(argument=argument)
    scope = {'callback': callback}
    exec(code, scope)
    __new__ = scope['__new__']
    return __new__


def make_init(argument):

    template = 'def __init__(self, {argument}): pass'
    code = template.format(argument=argument)
    scope = {}
    exec(code, scope)
    __init__ = scope['__init__']
    return __init__


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
                'Multiple inheritance is allowed for Injector subclasses only'
            )


def check_dunder_name(name):

    if name.startswith('__') and name.endswith('__'):
        raise DependencyError('Magic methods are not allowed')


def check_attrs_redefinition(name):

    for attr in ['let', 'use']:
        if name == attr:
            raise DependencyError(
                '{0!r} redefinition is not allowed'.format(attr)
            )


def check_cls_arguments(argnames, defaults):

    for name, value in zip(reversed(argnames), reversed(defaults)):
        expect_class = name.endswith('_cls')
        is_class = inspect.isclass(value)
        if expect_class and not is_class:
            raise DependencyError(
                '{0!r} default value should be a class'
                .format(name)
            )
        if not expect_class and is_class:
            raise DependencyError(
                "{0!r} argument can not have class as its default value"
                .format(name)
            )


def check_varargs(dependency, varargs, kwargs):

    if varargs and kwargs:
        raise DependencyError(
            '{0}.__init__ have arbitrary argument list and keyword arguments'
            .format(dependency.__name__)
        )
    elif varargs:
        raise DependencyError(
            '{0}.__init__ have arbitrary argument list'
            .format(dependency.__name__)
        )
    elif kwargs:
        raise DependencyError(
            '{0}.__init__ have arbitrary keyword arguments'
            .format(dependency.__name__)
        )


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
            raise DependencyError(
                '{0!r} is a circle dependency in the {1!r} constructor'
                .format(origin, attribute.__name__)
            )
        for name in args:
            check_circles_for(dependencies, name, origin)


def check_empty(argname, arg):

    if not arg:
        raise DependencyError(
            "'{argname}' argument can not be empty"
            .format(argname=argname)
        )
