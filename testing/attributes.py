import functools

import pytest


class _Touch:
    def __init__(self, access, assign, delete):
        self.access = access
        self.assign = assign
        self.delete = delete

    def __call__(self, *args):
        return self.access(*args)


def _context(f):
    @functools.wraps(f)
    def inner(*args):
        with args[0] as scope:
            return f(scope, *args[1:])

    return inner


@pytest.fixture(
    params=[
        _Touch(getattr, setattr, delattr),
        _Touch(_context(getattr), _context(setattr), _context(delattr)),
    ]
)
def touch(request):
    """Touch object attribute."""
    return request.param
