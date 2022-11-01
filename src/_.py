"""Declarative import statements designed for dependency injection."""


def __getattr__(name):
    from dependencies import Package

    return Package(name, _DO_NOT_USE_THIS_FLAG_=False)
