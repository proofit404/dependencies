from collections import deque


class _State:
    def __init__(self, cache, attrname):
        self.cache = cache
        self.tried = set()
        self.stack = deque()
        self.current = attrname
        self.have_default = False

    def add(self, current, have_default):
        self.stack.append((self.current, self.have_default))
        self.current = current
        self.have_default = have_default

    def pop(self):
        self.tried.add(self.current)
        try:
            self.current, self.have_default = self.stack.pop()
        except IndexError:
            pass

    def store(self, value):
        self.cache[self.current] = value
        self.pop()

    def resolved(self, required, optional):
        has_required = required <= self.cache.keys()
        tried_optional = optional <= self.tried
        return has_required and tried_optional

    def kwargs(self, args):
        return {k: self.cache[k] for k in args if k in self.cache}

    def should(self, arg, have_default):
        return arg not in self.tried or (arg not in self.cache and not have_default)

    def __repr__(self):
        indentation = _Indentation()
        name = self.cache["__self__"].__class__.__name__
        attributes = [attrname for attrname, have_default in self.stack]
        attributes.append(self.current)
        return "\n".join(f"{indentation()}{name}.{attrname}" for attrname in attributes)


class _Indentation:
    def __init__(self):
        self.index = 0

    def __call__(self):
        result = "  " * self.index
        self.index += 1
        return result
