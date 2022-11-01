"""Declarative import statements designed for dependency injection."""


def __getattr__(name):
    from dependencies import Package

    return Package(name)
