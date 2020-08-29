"""Dependency Injection for Humans."""
from _dependencies.injector import Injector
from _dependencies.operation import Operation as operation
from _dependencies.package import Package
from _dependencies.this import this
from _dependencies.value import Value as value


__all__ = ["Injector", "operation", "Package", "this", "value"]
