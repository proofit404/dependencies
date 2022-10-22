class Null:
    """Empty class."""


class StarArgs:
    """Wrong constructor signature."""

    def __init__(self, *args):
        self.args = args


class _Has(type):
    def __getitem__(self, item):
        from dataclasses import make_dataclass

        assert isinstance(item, str)
        cls = make_dataclass("cls", [item])
        return cls


class Has(metaclass=_Has):
    """Class holding an attribute."""

    def __init__(self):
        raise RuntimeError


del _Has


class _Take(type):
    def __getitem__(self, item):
        from dataclasses import make_dataclass

        assert isinstance(item, str)
        cls = make_dataclass("cls", [item])
        cls.__new__ = lambda cls, **kwargs: kwargs[item]
        return cls


class Take(metaclass=_Take):
    """Placeholder class."""

    def __init__(self):
        raise RuntimeError


del _Take
