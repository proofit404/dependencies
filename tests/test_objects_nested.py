"""Tests related to Injector classes written inside other Injector classes."""


def test_one_subcontainer_multiple_parents(define, let, has, expect, name):
    """Same sub container can be used in many parent containers.

    This usage should not overlap those containers. And more importantly, sub container
    should not be modified after usage.

    """
    root = define.cls(
        "Root", let.fun("__init__", "self, result", "self.result = result")
    )
    baz = define.cls("Baz", let.fun("__init__", "self, bar", "raise RuntimeError"))

    nested = has(bar="(this << 1).foo", baz=baz)
    it1 = has(root=root, result="this.sub.bar", sub=nested, foo="1")
    it2 = has(root=root, result="this.sub.bar", sub=nested, foo="2")

    expect(it1).to("obj.root.result == 1")
    expect(it2).to("obj.root.result == 2")

    message = f"""
You tried to shift this more times than Injector has levels:

{name(nested)}.baz
  {name(nested)}.bar
    """.strip()
    expect(nested).to_raise(message).when("obj.baz")


def test_deny_classes_depend_on_nested_injectors(define, let, has, expect, name):
    """Classes should not receive nested injectors as arguments of constructors."""
    foo = define.cls("Foo", let.fun("__init__", "self, bar", "raise RuntimeError"))
    it = has(foo=foo, bar=has(baz="None"))
    message = f"""
Do not depend on nested injectors directly.

Use this object to access inner attributes of nested injector:

{name(it)}.foo
    """.strip()
    expect(it).to_raise(message).when("obj.foo")
