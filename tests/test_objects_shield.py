"""Tests related to Shield object."""
from dependencies import Injector
from dependencies import shield


def test_pass_args(e, expect):
    """Pass positional arguments."""

    class Container(Injector):
        result = shield(e.StarArgs, 1, 2)

    @expect(Container)
    def case(it):
        assert it.result.args == (1, 2)


# FIXME: Shield object should not pass integer to foo_class as part of
# the **kwargs statement. Maybe role of verification of resolved
# class-named dependencies should be assigned to the resolved
# storage. Also, this resolved class_named argument should not be
# visible to other dependencies with foo_class argument. Maybe it's
# UUID should be stored in global scope but referenced by shield
# object internally.
