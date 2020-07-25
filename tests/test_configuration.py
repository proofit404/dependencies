# -*- coding: utf-8 -*-
"""Tests related to the project configuration."""
import collections
import configparser
import datetime
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


def test_all_pyenv_versions_in_tox_environments():
    """Every version from pyenv lock file should be included into Tox."""
    tox_environments = {
        e.split("-")[0]
        for e in subprocess.check_output(["tox", "-l"]).decode().splitlines()
    }

    pyenv_versions = [
        "py{}{}".format(*v.split(".")[0:2])
        for v in open(".python-version").read().splitlines()
    ]

    for version in pyenv_versions:
        assert version in tox_environments


def test_tox_environments_use_max_base_python():
    """Verify base Python version specified for Tox environments.

    Every Tox environment with base Python version specified should
    use max Python version.

    Max Python version is assumed from the .python-versions file.

    """
    pyenv_version = max(
        sorted(
            "python{}.{}".format(*v.split(".")[0:2])
            for v in open(".python-version").read().splitlines()
        )
    )
    for _env, basepython in helpers.tox_info("basepython"):
        assert basepython == pyenv_version


def test_envlist_contains_all_tox_environments():
    """The envlist setting should contains all tox environments.

    It's not allowed to have tox environments defined without having them in the
    envlist.

    """
    tox_environments = set(subprocess.check_output(["tox", "-l"]).decode().splitlines())

    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    tox_ini = {
        k.replace("testenv:", "") for k in ini_parser if k.startswith("testenv:")
    }

    assert not tox_ini - tox_environments


def test_tox_generative_environments_has_common_definition():
    """Test envlist contains python environments together with plain testenv.

    The plain testenv definition is allowed only if envlist contains generative
    environments.

    """
    tox_environments = {
        "testenv"
        for e in subprocess.check_output(["tox", "-l"]).decode().splitlines()
        if re.match(r"\Apy\d{2}\Z", e.split("-")[0])
    }

    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    tox_ini = {e for e in ini_parser if e == "testenv"}

    assert tox_environments == tox_ini


def test_single_line_settings_are_written_same_line():
    """Single line tox settings should be written on the same line."""
    single_line_settings = [
        "isolated_build",
        "basepython",
        "skip_install",
        "install_command",
    ]

    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser.values():
        for setting in single_line_settings:
            value = section.get(setting)
            if value is not None:
                assert not value.startswith("\n")


def test_tox_multiline_settings_are_written_next_line():
    """Multiline tox settings should be written starting next line."""
    multiline_settings = [
        "commands",
        "commands_post",
        "depends",
        "deps",
        "envlist",
        "whitelist_externals",
    ]

    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser.values():
        for setting in multiline_settings:
            value = section.get(setting)
            if value is not None:
                assert value.startswith("\n") or not value


def test_coverage_include_all_packages():
    """Coverage source should include all packages.

    1. From the main pyproject.toml.
    2. From test helpers pyproject.toml.
    3. The tests package.

    """
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".coveragerc")
    coverage_sources = ini_parser["run"]["source"].strip().splitlines()

    pyproject_toml = tomlkit.loads(open("pyproject.toml").read())
    packages = [
        re.sub(r"\.py$", "", p["include"])
        for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    pyproject_toml = tomlkit.loads(open("tests/helpers/pyproject.toml").read())
    helpers = [
        re.sub(r"\.py$", "", p["include"])
        for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    assert coverage_sources == packages + helpers + ["tests"]


def test_coverage_paths_include_tox_environments():
    """Coverage paths should include all tox environments."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".coveragerc")
    coverage_paths = ini_parser["paths"]["source"].strip().splitlines()

    tox_environments = subprocess.check_output(["tox", "-l"]).decode().splitlines()
    tox_ini = configparser.ConfigParser()
    tox_ini.read("tox.ini")
    coverage_environments = [
        e
        for e in tox_environments
        if "coverage run"
        in tox_ini["testenv:" + e if "testenv:" + e in tox_ini else "testenv"][
            "commands"
        ]
    ]
    tox_paths = [
        ".tox/{name}/lib/{python}/site-packages".format(
            name=e,
            python=tox_ini["testenv:" + e]["basepython"]
            if "testenv:" + e in tox_ini
            else re.sub(
                r"py(?P<major>\d)(?P<minor>\d)",
                r"python\g<major>.\g<minor>",
                e.split("-")[0],
            ),
        )
        for e in coverage_environments
    ]

    assert coverage_paths == tox_paths


def test_coverage_environment_runs_at_the_end():
    """Covarage report should runs after environments generating coverage."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")

    envlist = helpers.tox_parse_envlist(ini_parser["tox"]["envlist"])

    runs_coverage = [
        e
        for e in envlist
        if "coverage run"
        in ini_parser["testenv:" + e if "testenv:" + e in ini_parser else "testenv"][
            "commands"
        ]
    ]

    coverage_depends = helpers.tox_parse_envlist(
        ini_parser["testenv:coverage"]["depends"]
    )

    assert coverage_depends == runs_coverage


def test_ini_files_indentation():
    """INI files should have indentation level equals two spaces."""
    for ini_file in [
        ".coveragerc",
        ".flake8",
        ".importlinter",
        "pytest.ini",
        "tox.ini",
    ]:
        ini_text = open(ini_file).read()
        assert not re.search(r"^ \S", ini_text, re.MULTILINE)
        assert not re.search(r"^ {3}", ini_text, re.MULTILINE)


def test_lock_files_not_committed():
    """Lock files should not be committed to the git repository."""
    git_files = subprocess.check_output(["git", "ls-files"]).decode().splitlines()
    for lock_file in ["poetry.lock", "tests/helpers/poetry.lock"]:
        assert lock_file not in git_files


def test_license_year():
    """The year in the license notes should be the current year."""
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


# Definition order.


def test_tox_environments_are_ordered():
    """Tox environments definition should follow order of the envlist."""
    tox_environments = subprocess.check_output(["tox", "-l"]).decode().splitlines()

    tox_ini = open("tox.ini").read()

    offsets = [
        (tox_ini.find("testenv{}".format("" if re.match(r"py\d+", e) else ":" + e)), e)
        for e in tox_environments
    ]

    assert offsets == sorted(offsets, key=lambda key: key[0])


def test_tox_deps_are_ordered():
    """Dependencies of tox environments should be in order."""
    for _env, deps in helpers.tox_info("deps"):
        deps = [d.split("==")[0] for d in deps.splitlines()]
        ordered = [
            deps[l[1]]
            for l in sorted(
                (
                    [list(map(lambda x: x.strip().lower(), reversed(d.split(":")))), i]
                    for i, d in enumerate(deps)
                ),
                key=lambda key: key[0],
            )
        ]
        assert deps == ordered


def test_packages_are_ordered():
    """Packages of pyproject.toml files should be in order."""
    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        packages = [
            re.sub(r"\.py$", "", p["include"])
            for p in pyproject_toml["tool"]["poetry"]["packages"]
        ]
        assert packages == sorted(packages)


def test_build_requires_are_ordered():
    """Build system requirements of pyproject.toml files should be in order."""
    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        requires = pyproject_toml["build-system"]["requires"]
        assert requires == sorted(requires)


def test_flake8_per_file_ignores_are_ordered():
    """Flake8 per file ignores should be in order."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".flake8")
    per_file_ignores = [
        l.strip()
        for l in ini_parser["flake8"]["per-file-ignores"].strip().splitlines()
        if not l.startswith("#")
    ]
    assert per_file_ignores == sorted(per_file_ignores)


@pytest.mark.xfail
def test_flake8_ignored_errors_are_ordered():  # pragma: no cover
    """Flake8 ignored error codes should be in order."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".flake8")
    ignore = ini_parser["flake8"]["ignore"].strip().split(", ")
    assert ignore == sorted(ignore)


def test_yamllint_ignored_patterns_are_ordered():
    """Yamllint ignored directory patterns should be in order."""
    yamllint = yaml.safe_load(open(".yamllint").read())
    ignore = [l.strip() for l in yamllint["ignore"].strip().splitlines()]
    assert ignore == sorted(ignore)


# Additional dependencies.


def test_poetry_avoid_additional_dependencies():
    """Python package should not have any of additional dependencies."""
    pyproject_toml = tomlkit.loads(open("pyproject.toml").read())
    deps = list(pyproject_toml["tool"]["poetry"].get("dependencies", {}))
    assert deps == ["python"]

    pyproject_toml = tomlkit.loads(open("tests/helpers/pyproject.toml").read())
    deps = list(pyproject_toml["tool"]["poetry"].get("dependencies", {}))
    assert not deps


def test_pre_commit_hooks_avoid_additional_dependencies():
    """Additional dependencies of the pre-commit should not be used."""
    pre_commit_config_yaml = yaml.safe_load(open(".pre-commit-config.yaml").read())
    hooks = (hook for repo in pre_commit_config_yaml["repos"] for hook in repo["hooks"])
    assert all("additional_dependencies" not in hook for hook in hooks)


# Version pinning.


def test_tox_deps_not_pinned():
    """Dependencies of tox environments should not have versions."""
    for _env, deps in helpers.tox_info("deps"):
        deps = deps.splitlines()
        deps = [d.split(":")[-1].strip().split("==") for d in deps]
        versions = collections.defaultdict(list)
        for d in deps:
            versions[d[0]].append(d[-1] if d[1:] else "*")
        for _package, v in versions.items():
            assert v == ["*"] or len(v) >= 2


def test_build_requires_not_pinned():
    """Build requirements of pyproject.toml files should not have versions."""
    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        requires = pyproject_toml["build-system"]["requires"]
        for require in requires:
            assert len(re.split(r"=+", require)) == 1


def test_pre_commit_hooks_not_pinned():
    """Hook revisions of the pre-commit should not have versions."""
    pre_commit_config_yaml = yaml.safe_load(open(".pre-commit-config.yaml").read())
    assert all(repo["rev"] == "master" for repo in pre_commit_config_yaml["repos"])
