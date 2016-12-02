class CodeCollector(object):

    def __init__(self):

        self.collected = []

    def __call__(self, f):

        self.collected.append(f)

    def __iter__(self):

        return iter(self.collected)
