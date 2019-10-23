import configparser
import textwrap

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


def tox_info(var):
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if var in ini_parser[section]:
            value = textwrap.dedent(ini_parser[section][var].strip())
            yield section, value
