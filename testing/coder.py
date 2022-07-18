import pytest

from rnd import _rnd


class _Module:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"{self.path.stem}"

    def __repr__(self):
        return repr(f"{self.path.parent.stem}.{self.path.stem}")

    def write(self, code):
        assert "\n" in code
        self._write("\n\n")
        self._write(str(code))

    def _write(self, code):
        with self.path.open("a") as tests:
            tests.write(code)


class _Coder:
    def __init__(self, pytester):
        self.pytester = pytester
        self.path = pytester.path.joinpath("test_case.py")
        self._write("import pytest\n")
        self._write("from dependencies import *\n")
        self._write("from dependencies.exceptions import *\n")

    write = _Module.write
    _write = _Module._write

    def module(self):
        return _Module(self.pytester.mkpydir(_rnd()).joinpath(_rnd()))

    def run(self):
        print(self.path.read_text())
        result = self.pytester.runpytest()
        assert result.ret is pytest.ExitCode.OK
        result.assert_outcomes(passed=1)


@pytest.fixture()
def coder(pytester):
    """Wride python tests in different ways."""
    return _Coder(pytester)
