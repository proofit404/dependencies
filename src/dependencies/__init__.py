"""Constructor injection designed with OOP in mind."""
from _dependencies.injector import Injector
from _dependencies.objects.shield import shield
from _dependencies.objects.value import value


__all__ = ("Injector", "value", "shield")
