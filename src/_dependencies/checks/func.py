import inspect

from _dependencies.exceptions import DependencyError


def check_cls_arguments(argnames, defaults, owner_message):

    for argument, value in zip(reversed(argnames), reversed(defaults)):
        expect_class = argument.endswith("_class")
        is_class = inspect.isclass(value)
        if expect_class and not is_class:
            message = "{0!r} default value should be a class"
            raise DependencyError(message.format(argument))
        if not expect_class and is_class:
            message = default_class_value_template.format(
                owner_message=owner_message, argument=argument, value=value.__name__
            )
            raise DependencyError(message)


def check_varargs(name, varargs, kwargs):

    if varargs and kwargs:
        message = "{0} have arbitrary argument list and keyword arguments"
        raise DependencyError(message.format(name))
    elif varargs:
        message = "{0} have arbitrary argument list"
        raise DependencyError(message.format(name))
    elif kwargs:
        message = "{0} have arbitrary keyword arguments"
        raise DependencyError(message.format(name))


# Messages.


default_class_value_template = """
{owner_message} has a default value of {argument!r} argument set to {value!r} class.

You should either change the name of the argument into '{argument}_class'
or set the default value to an instance of that class.
""".strip()
