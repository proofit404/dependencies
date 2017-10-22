from inspect import getdoc

import pytest


class CodeCollector(object):

    def __init__(self):

        self.collected = []

    def __call__(self, f):

        self.collected.append(f)
        return f

    def __iter__(self):

        return iter(self.collected)

    def parametrize(self, test_func):

        return pytest.mark.parametrize('code', self, ids=getdoc)(test_func)
