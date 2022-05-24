from _dependencies.enclose import _Enclose


class _Stack:
    def __init__(self):
        self.queue = []

    def add(self):
        enclose = _Enclose()
        self.queue.append(enclose)
        return enclose

    def remove(self):
        enclose = self.queue.pop()
        enclose.after()
