from _dependencies.attributes import Attributes
from _dependencies.spec import make_dependency_spec


def deep_replace_dependency(injector, current_attr, replace):

    spec = make_dependency_spec(current_attr, replace.dependency)
    marker, attribute, args, have_defaults = spec
    attribute = Attributes(attribute, replace.attrs)
    spec = (marker, attribute, args, have_defaults)

    for base in injector.__mro__:
        if current_attr in base.__dependencies__:
            base.__dependencies__[current_attr] = spec
        else:
            break
