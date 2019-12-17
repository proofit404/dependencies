import collections
import configparser
import datetime
import itertools
import json
import re
import subprocess
import sys

import pytest
import tomlkit
import yaml

import helpers

# This is a little bit a workaround of the PyYaml library limitations.
# It doesn't preserve the order of keys of the parsed dict.  It works
# on recent Python versions where the order of keys is guaranteed by
# dict implementation.  See https://github.com/yaml/pyyaml/issues/110
# for more info.
pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 6), reason="These tests rely on the order of the dict keys"
)


def test_tox_environments_order():
    """
    The definition of the tox environments should follow envlist.
    """

    tox_environments = subprocess.check_output(["tox", "-l"]).decode().splitlines()

    tox_ini = open("tox.ini").read()

    offsets = [
        (tox_ini.find("testenv{}".format("" if re.match(r"py\d+", e) else ":" + e)), e)
        for e in tox_environments
    ]

    assert offsets == sorted(offsets, key=lambda key: key[0])


def test_tox_environments_includes_python_versions():
    """
    All versions from pyenv lock file should be included into Tox environments.
    """

    tox_environments = set(
        itertools.chain.from_iterable(
            e.split("-")
            for e in subprocess.check_output(["tox", "-l"]).decode().splitlines()
        )
    )

    pyenv_versions = [
        "py{}{}".format(*v.split(".")[0:2])
        for v in open(".python-version").read().splitlines()
    ]

    for version in pyenv_versions:
        assert version in tox_environments


def test_tox_environments_equal_azure_tasks():
    """
    Every tox environment should be precent in the Azure Pipeline task list.

    The order should be preserved.
    """

    tox_environments = subprocess.check_output(["tox", "-l"]).decode().splitlines()

    azure_pipelines = yaml.safe_load(open("azure-pipelines.yml").read())
    azure_tasks = [
        v["tox.env"] for v in azure_pipelines["jobs"][0]["strategy"]["matrix"].values()
    ]

    assert tox_environments == azure_tasks


def test_tox_environment_base_python_equal_azure_task_python_version():
    """
    If tox environment has `basepython` setting, the corresponding
    Azure Pipeline task should has the same value in the `python.version`
    setting.
    """

    azure_pipelines = yaml.safe_load(open("azure-pipelines.yml").read())
    azure_tasks = {
        k: v["python.version"]
        for k, v in azure_pipelines["jobs"][0]["strategy"]["matrix"].items()
    }

    for env, basepython in helpers.tox_info("basepython"):
        env = re.sub(r"^testenv:", "", env)
        basepython = re.sub(r"^python", "", basepython)
        assert basepython == azure_tasks[env]


def test_tox_deps_are_ordered():
    """
    Dependencies section of all tox environments should be in alphabetical order.
    """

    for _env, deps in helpers.tox_info("deps"):
        deps = [d.split("==")[0] for d in deps.splitlines()]
        ordered = [
            deps[l[1]]
            for l in sorted(
                [
                    [list(map(lambda x: x.strip().lower(), reversed(d.split(":")))), i]
                    for i, d in enumerate(deps)
                ],
                key=lambda key: key[0],
            )
        ]
        assert deps == ordered


def test_nodejs_deps_are_ordered():
    """
    Development dependencies of the package.json should be in alphabetical order.
    """

    package_json = json.load(open("package.json"))
    deps = list(package_json["devDependencies"].keys())
    assert deps == sorted(deps)


def test_poetry_deps_are_ordered():
    """
    Dependencies section of all pyproject.toml files should be in
    alphabetical order.
    """

    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        deps = list(pyproject_toml["tool"]["poetry"].get("dependencies", {}))
        if deps:
            assert deps == ["python"] + sorted(deps[1:])


def test_packages_are_ordered():
    """
    Packages section of all pyproject.toml files should be in alphabetical order.
    """

    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        packages = [
            p["include"].rstrip(".py")
            for p in pyproject_toml["tool"]["poetry"]["packages"]
        ]
        assert packages == sorted(packages)


def test_build_requires_are_ordered():
    """
    Requirements of the build system of all pyproject.toml files
    should be in alphabetical order.
    """
    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        requires = pyproject_toml["build-system"]["requires"]
        assert requires == sorted(requires)


def test_pre_commit_hooks_avoid_additional_dependencies():
    """
    Additional dependencies section of all hooks of all repositories
    of the .pre-commit-config.yaml should not be used.
    """
    # There is no special policy related to the additional
    # dependencies in the pre-commit hooks.  At the time of writing
    # there were no additional dependencies in all hooks in all
    # repositories.  If you need to include additional dependency to
    # the hook, please replace this test with two tests:
    #
    # * additional dependencies are ordered
    #
    # * additional dependencies have no pinned versions

    pre_commit_config_yaml = yaml.safe_load(open(".pre-commit-config.yaml").read())
    hooks = (hook for repo in pre_commit_config_yaml["repos"] for hook in repo["hooks"])
    assert all("additional_dependencies" not in hook for hook in hooks)


def test_tox_deps_not_pinned():
    """
    Dependencies section of all tox environments should not have version specified.
    """

    for _env, deps in helpers.tox_info("deps"):
        deps = deps.splitlines()
        deps = [d.split(":")[-1].strip().split("==") for d in deps]
        versions = collections.defaultdict(list)
        for d in deps:
            versions[d[0]].append(d[-1] if d[1:] else "*")
        for _package, v in versions.items():
            assert v == ["*"] or len(v) >= 2


def test_nodejs_deps_not_pinned():
    """
    Development dependencies of the package.json should not have version specified.
    """

    package_json = json.load(open("package.json"))
    versions = list(package_json["devDependencies"].values())
    assert all(v == "*" for v in versions)


def test_poetry_deps_not_pinned():
    """
    Dependencies section of all pyproject.toml files should not have version specified.
    """

    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        versions = [
            d.get("version")
            for d in pyproject_toml["tool"]["poetry"].get("dependencies", {}).values()
            if isinstance(d, dict)
        ]
        assert all(v == "*" for v in versions)


def test_build_requires_not_pinned():
    """
    Requirements of the build system of all pyproject.toml files
    should not have version specified.
    """
    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        requires = pyproject_toml["build-system"]["requires"]
        for require in requires:
            assert len(re.split(r"=+", require)) == 1


def test_pre_commit_hooks_not_pinned():
    """
    Hook revisions of the .pre-commit-config.yaml should not have tag specified.
    """

    pre_commit_config_yaml = yaml.safe_load(open(".pre-commit-config.yaml").read())
    assert all(repo["rev"] == "" for repo in pre_commit_config_yaml["repos"])


def test_coverage_include_all_packages():
    """
    Coverage source should include packages:

    * from the main pyproject.toml,
    * from test helpers pyproject.toml,
    * the tests package
    """

    ini_parser = configparser.ConfigParser()
    ini_parser.read(".coveragerc")
    coverage_sources = ini_parser["run"]["source"].strip().splitlines()

    pyproject_toml = tomlkit.loads(open("pyproject.toml").read())
    packages = [
        p["include"].rstrip(".py") for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    pyproject_toml = tomlkit.loads(open("tests/helpers/pyproject.toml").read())
    helpers = [
        p["include"].rstrip(".py") for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    assert coverage_sources == packages + helpers + ["tests"]


def test_ini_files_indentation():
    """
    All ini files should have indentation level equals two spaces.
    """

    for ini_file in [
        ".coveragerc",
        ".flake8",
        ".importlinter",
        "mypy.ini",
        "pytest.ini",
        "tox.ini",
    ]:
        ini_text = open(ini_file).read()
        assert not re.search(r"^   ", ini_text, re.MULTILINE)


def test_lock_files_not_committed():
    """
    Lock files should not be committed to the git repository.
    """

    git_files = subprocess.check_output(["git", "ls-files"]).decode().splitlines()
    for lock_file in ["poetry.lock", "tests/helpers/poetry.lock", "package-lock.json"]:
        assert lock_file not in git_files


def test_license_year():
    """
    The year in the license notes should be the current year.
    """

    current_year = datetime.date.today().year
    lines = [
        l.split(":", 1)
        for l in subprocess.check_output(["git", "grep", "-i", "copyright"])
        .decode()
        .splitlines()
    ]
    for _filename, line in lines:
        found = re.findall(r"\b\d{4}\b", line)
        if found:
            year = int(found[-1])
            assert year == current_year
