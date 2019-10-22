import configparser

import pytest


class CodeCollector(object):
    def __init__(self, name="code"):

        self.name = name
        self.collected = []

    def __call__(self, f):

        self.collected.append(f)
        return f

    def xfail(self, f):

        self(pytest.param(f, marks=pytest.mark.xfail))
        return f

    def __iter__(self):

        return iter(self.collected)

    def parametrize(self, test_func):

        return pytest.mark.parametrize(self.name, self)(test_func)


def get_tox_deps():
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if "deps" in ini_parser[section]:
            deps = ini_parser[section]["deps"].strip().splitlines()
            yield deps
