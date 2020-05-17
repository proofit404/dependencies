# -*- coding: utf-8 -*-
import configparser
import re
import textwrap

import pytest


class CodeCollector(object):
    """Dedicated decorator to use functions as Py.Test function parameters."""

    def __init__(self, name="code"):

        self.name = name
        self.collected = []

    def __call__(self, f):
        """Mark decorated function as a test parameter."""
        self.collected.append(f)
        return f

    def xfail(self, f):
        """Mark function as a test parameter with expected failure."""
        return self(pytest.param(f, marks=pytest.mark.xfail))

    def __iter__(self):
        return iter(self.collected)

    def parametrize(self, test_func):
        """Parametrize decorated test function with collected functions."""
        return pytest.mark.parametrize(self.name, self)(test_func)


def tox_info(var):
    """Get variable value from all sections in the tox.ini file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if var in ini_parser[section]:
            value = textwrap.dedent(ini_parser[section][var].strip())
            yield section, value


def tox_parse_envlist(string):
    """Parse tox environment list with proper comma escaping."""
    escaped = string
    while re.search(r"({[^,}]*),", escaped):
        escaped = re.subn(r"({[^,}]*),", r"\1:", escaped)[0]
    parts = escaped.split(",")
    return [re.subn(r":", ",", p)[0].strip() for p in parts]
