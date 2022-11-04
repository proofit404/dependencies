class Null:
    """Empty class."""


class StarArgs:
    """Wrong constructor signature."""

    def __init__(self, *args):
        self.args = args


class _Has(type):
    # FIXME: Rewrite this class into concept of multiple predefined
    # HasA, HasB, HasAB classes.
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
    # FIXME: Drop these concept. Direct resolve rule was removed
    # previousy, which existence was the entire reason we need this
    # class.
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
