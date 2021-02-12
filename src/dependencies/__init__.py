"""Dependency Injection for Humans."""
from _dependencies.injector import Injector
from _dependencies.kinds.package import Package
from _dependencies.kinds.this import this
from _dependencies.kinds.value import Value as value


__all__ = ["Injector", "Package", "this", "value"]
