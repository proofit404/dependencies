# -*- coding: utf-8 -*-
from _dependencies.exceptions import DependencyError


def check_inheritance(bases, injector):

    for base in bases:
        if not issubclass(base, injector):
            message = "Multiple inheritance is allowed for Injector subclasses only"
            raise DependencyError(message)


def check_dunder_name(name):

    if name.startswith("__") and name.endswith("__"):
        raise DependencyError("Magic methods are not allowed")


def check_attrs_redefinition(name):

    if name == "let":
        raise DependencyError("'let' redefinition is not allowed")
