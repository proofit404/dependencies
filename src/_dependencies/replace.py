from _dependencies.attributes import _Attributes
from _dependencies.spec import _make_dependency_spec


def _deep_replace_dependency(injector, current_attr, replace):

    spec = _make_dependency_spec(current_attr, replace.dependency)
    marker, attribute, args, required, optional = spec
    attribute = _Attributes(attribute, replace.attrs)
    spec = (marker, attribute, args, required, optional)

    for base in injector.__mro__:
        if current_attr in base.__dependencies__:
            base.__dependencies__[current_attr] = spec
        else:
            break
