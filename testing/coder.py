import pytest

from rnd import _rnd


class _File:
    def __init__(self, path):
        self.path = path
        self.separator = ""

    def write(self, code):
        self._write(self.separator)
        self._write(str(code).strip() + "\n")

    def _write(self, code):
        with self.path.open("a") as tests:
            tests.write(code)
        self.separator = "\n\n"


class _Module(_File):
    def __str__(self):
        return f"{self.path.stem}"

    def __repr__(self):
        return repr(f"{self.path.parent.stem}.{self.path.stem}")


class _Coder(_File):
    def __init__(self, pytester):
        super().__init__(pytester.path.joinpath("test_case.py"))
        self.pytester = pytester
        self.modules = []
        self.write(
            """
import pytest
from dependencies import *
from dependencies.exceptions import *
            """
        )

    def module(self):
        module = _Module(self.pytester.mkpydir(_rnd()).joinpath(_rnd() + ".py"))
        self.modules.append(module)
        return module

    def run(self):
        for module in self.modules:
            print(module.path.read_text(), end="")
            print("-" * 80)
        print(self.path.read_text(), end="")
        result = self.pytester.runpytest()
        assert result.ret is pytest.ExitCode.OK
        result.assert_outcomes(passed=1)


@pytest.fixture()
def coder(pytester):
    """Wride python tests in different ways."""
    return _Coder(pytester)
