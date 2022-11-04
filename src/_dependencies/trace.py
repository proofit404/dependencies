class _Trace:
    def __init__(self, state):
        self.states = [state]

    def __str__(self):
        indentation = _Indentation()
        return self.error + ":\n\n" + "\n".join(map(indentation, self.stack()))

    def add(self, error):
        self.error = error

    def stack(self):
        attributes = []
        seen = set()
        for state in self.states:
            scope = state.cache["__self__"]
            name = scope.__class__.__name__
            for attribute in [*[s[0] for s in state.stack], state.current]:
                attributes.append(f"{name}.{attribute}")
                if (scope, attribute) in seen:  # pragma: no cover
                    return attributes
                else:
                    seen.add((scope, attribute))
        return attributes


class _Indentation:
    def __init__(self):
        self.index = 0

    def __call__(self, arg):
        result = "  " * self.index + arg
        self.index += 1
        return result
