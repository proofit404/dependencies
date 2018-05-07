from dependencies import Injector, operation


def test_define_operation():
    """Create operation from the function definition."""

    class Container(Injector):

        foo = 1
        bar = 2
        baz = 3

        @operation
        def process(foo, bar, baz):
            return foo + bar + baz

    assert Container.process() == 6


# TODO: Raise exception if `self` was found in the arguments.
#
# TODO: Raise exception if we try to decorate a class.
#
# TODO: Operation representation with the name of the function.
#
# TODO: Support default keyword arguments.
