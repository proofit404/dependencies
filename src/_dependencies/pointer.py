class _Pointer:
    def __getattr__(self, attrname):
        return self.resolver.__class__(
            self.resolver.graph, self.resolver.state.cache, attrname
        ).resolve()
