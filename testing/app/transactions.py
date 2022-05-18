log = __builtins__["print"]


class Transactional:
    """Service wrapper."""

    def __init__(self, service):
        self.service = service

    def __repr__(self):
        return f"{self.__class__.__name__}({self.service!r})"

    def commit(self):
        """Perform database commit."""
        if self.service.success:
            log("DONE")
        else:
            log("FAIL")

    def __getattr__(self, name):
        return getattr(self.service, name)
