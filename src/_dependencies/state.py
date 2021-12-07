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
