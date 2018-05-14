import importlib
import inspect

from ._spec import make_init_spec, use_object_init


def Package(name):

    return PackageType("Package", (object,), {"__modulename__": name})


class PackageType(type):

    def __new__(cls, class_name, bases, namespace):

        module = importlib.import_module(namespace["__modulename__"])

        def __new__(cls):
            return module

        def __init__(self):
            pass

        namespace.update({"__new__": __new__, "__init__": __init__})
        return type.__new__(cls, class_name, bases, namespace)

    def __getattr__(cls, attrname):

        try:
            name = cls.__modulename__ + "." + attrname
            return PackageType(cls.__name__, cls.__bases__, {"__modulename__": name})
        except ImportError:
            return AttributeType(
                "Attribute",
                (object,),
                {
                    "__modulename__": cls.__modulename__,
                    "__variable__": attrname,
                    "__attributes__": [],
                },
            )


class AttributeType(type):

    def __new__(cls, class_name, bases, namespace):

        module = importlib.import_module(namespace["__modulename__"])
        attribute = getattr(module, namespace["__variable__"])

        if inspect.isclass(attribute):
            __new__ = make_new(attribute, namespace["__attributes__"])
            __init__ = make_init(attribute)
        else:

            def __new__(cls):
                value = attribute
                for attrname in namespace["__attributes__"]:
                    value = getattr(value, attrname)
                return value

            def __init__(self):
                pass

        namespace.update({"__new__": __new__, "__init__": __init__})
        return type.__new__(cls, class_name, bases, namespace)

    def __getattr__(cls, attrname):

        return AttributeType(
            cls.__name__,
            cls.__bases__,
            {
                "__modulename__": cls.__modulename__,
                "__variable__": cls.__variable__,
                "__attributes__": cls.__attributes__ + [attrname],
            },
        )


def make_new(cls, attributes):

    arguments = get_arguments(cls)
    code = new_template.format(arguments=arguments)
    scope = {"__origin__": cls, "__attributes__": attributes}
    exec(code, scope)
    __new__ = scope["__new__"]
    return __new__


def make_init(cls):

    arguments = get_arguments(cls)
    template = "def __init__(self, {arguments}): pass"
    code = template.format(arguments=arguments)
    scope = {}
    exec(code, scope)
    __init__ = scope["__init__"]
    return __init__


def get_arguments(cls):

    if use_object_init(cls):
        return ""
    else:
        return ", ".join(make_init_spec(cls)[0])


new_template = """def __new__(cls, {arguments}):
    value = __origin__({arguments})
    for attrname in __attributes__:
        value = getattr(value, attrname)
    return value
"""
