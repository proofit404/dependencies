"""Constructor injection designed with OOP in mind."""
from _dependencies.injector import Injector
from _dependencies.objects.package import Package
from _dependencies.objects.shield import shield
from _dependencies.objects.this import this
from _dependencies.objects.value import value


__all__ = ("Injector", "Package", "this", "value", "shield")
