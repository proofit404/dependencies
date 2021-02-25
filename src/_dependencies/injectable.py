from inspect import isclass
from inspect import Parameter
from inspect import signature

from _dependencies.exceptions import DependencyError


def _function_args(func, funcname, owner):
    arguments = _args(func, funcname, owner)
    return _separate(arguments)


def _method_args(func, funcname, owner):
    arguments = _args(func, funcname, owner)
    return _separate(arguments[1:])


def _args(func, funcname, owner):
    args = []
    errors = {
        Parameter.VAR_POSITIONAL: "{!r} have variable-length positional arguments",
        Parameter.VAR_KEYWORD: "{!r} have variable-length keyword arguments",
        Parameter.POSITIONAL_ONLY: "{!r} have positional-only arguments",
    }
    for name, param in signature(func).parameters.items():
        have_default = param.default is not param.empty
        args.append((name, have_default))
        if have_default:
            _check_argument_default(name, param.default, owner)
        if param.kind in errors:
            raise DependencyError(errors[param.kind].format(funcname))
    return args


def _separate(arguments):
    args = {}
    required = set()
    optional = set()
    for name, have_default in arguments:
        args[name] = have_default
        target = optional if have_default else required
        target.add(name)
    return args, required, optional


def _check_argument_default(argument, value, owner):
    expect_class = argument.endswith("_class")
    is_class = isclass(value)
    if expect_class and not is_class:
        message = "{0!r} default value should be a class"
        raise DependencyError(message.format(argument))
    if not expect_class and is_class:
        message = default_class_value_template.format(
            owner=owner, argument=argument, value=value.__name__
        )
        raise DependencyError(message)


# Messages.


default_class_value_template = """
{owner} has a default value of {argument!r} argument set to {value!r} class.

You should either change the name of the argument into '{argument}_class'
or set the default value to an instance of that class.
""".strip()
