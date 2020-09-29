class _Replace(Exception):
    def __init__(self, dependency):
        self.dependency = dependency
