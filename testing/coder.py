import pytest


class Coder:
    def __init__(self, pytester):
        self.pytester = pytester
        self._write(
            """
import pytest
from dependencies import *
from dependencies.exceptions import *
            """
        )

    def write(self, code):
        assert "\n" in code
        self._write("\n\n")
        self._write(str(code))

    def _write(self, code):
        with self.pytester.path.joinpath("test_case.py").open("a") as tests:
            tests.write(code)

    def run(self):
        print(self.pytester.path.joinpath("test_case.py").read_text())
        result = self.pytester.runpytest()
        assert result.ret is pytest.ExitCode.OK
        result.assert_outcomes(passed=1)


@pytest.fixture()
def coder(pytester):
    """Wride python tests in different ways."""
    return Coder(pytester)
