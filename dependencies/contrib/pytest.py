"""
dependencies.contrib.pytest
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Py.test fixtures.

:copyright: (c) 2016-2017 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from __future__ import absolute_import

import pytest

__all__ = ['register', 'require']


def register(injector):
    """Register Py.test fixture performing injection in it's scope."""

    if 'fixture' not in injector:
        raise AttributeError(
            "{0!r} object has no attribute 'fixture'".format(
                injector.__name__,
            ),
        )

    options = {'name': injector.name}

    for option in ['scope', 'params', 'autouse', 'ids']:
        if option in injector:
            options[option] = getattr(injector, option)

    @pytest.fixture(**options)
    def __fixture(request):

        return injector.let(request=request).fixture

    __fixture.injector = injector
    return __fixture


def require(fixturename):
    """Mark fixture as a dependency for injection process."""

    return type(
        Requirement.__name__,
        (Requirement,),
        {'fixturename': fixturename},
    )


class Requirement(object):

    fixturename = None

    def __new__(cls, request):

        return request.getfixturevalue(cls.fixturename)

    def __init__(self, request):

        pass
