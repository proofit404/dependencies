"""Tests related to the project configuration."""
import collections
import configparser
import datetime
import re
import subprocess
import textwrap

import tomlkit
import yaml


def test_tox_environments_use_all_pyenv_versions():
    """All python versions defined in .python-version file should be tested."""
    versions = [f"py{major}{minor}" for major, minor in pyenv_versions()]
    for version in versions:
        assert version in tox_envlist()


def test_tox_environments_use_max_base_python():
    """Environments not related to tests should use latest python version."""
    version = max(sorted(f"python{major}.{minor}" for major, minor in pyenv_versions()))
    for basepython in tox_config_values("basepython"):
        assert basepython.value == version


def test_tox_envlist_contains_all_tox_environments():
    """It's not allowed to define environments without envlist."""
    assert tox_envlist() == tox_config_environments()


def test_tox_no_default_environment():
    """Each environment should have dedicated definition."""
    assert "testenv" not in tox_ini()


def test_tox_no_factor_environments():
    """Do not use environment factors."""
    assert not any("-" in e for e in tox_envlist())


def test_tox_no_factor_deps():
    """Deny to use factors in dependencies."""
    for deps in tox_config_values("deps"):
        for dep in deps.value.splitlines():
            assert ":" not in dep


def test_single_line_settings_are_written_same_line():
    """Single line tox settings should be written on the same line."""
    single_line_settings = [
        "isolated_build",
        "basepython",
        "skip_install",
        "install_command",
    ]
    for section in tox_ini().values():
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
    for section in tox_ini().values():
        for setting in multiline_settings:
            value = section.get(setting)
            if value is not None:
                assert value.startswith("\n") or not value


def test_coverage_include_all_packages():
    """Code coverage should include all python packages."""
    coverage_sources = coveragerc()["run"]["source"].strip().splitlines()

    packages = set()
    helpers = set()

    for f in git_files():
        parts = [re.sub(r"\.py$", "", p) for p in f.split("/")]
        if len(parts) > 1 and parts[0] == "src":
            packages.add(parts[1])
        if len(parts) > 2 and parts[0] == "tests" and parts[1] == "helpers":
            helpers.add(parts[2])

    assert coverage_sources == sorted(packages) + sorted(helpers) + ["tests"]


def test_coverage_paths_include_tox_environments():
    """Coverage files should be merged together."""
    coverage_environments = [
        env
        for env, commands in tox_config_values("commands")
        if "coverage run" in commands
    ]
    tox_paths = [
        ".tox/{name}/lib/{python}/site-packages".format(
            name=e,
            python=tox_ini()["testenv:" + e]["basepython"]
            if "testenv:" + e in tox_ini()
            else re.sub(
                r"py(?P<major>\d)(?P<minor>\d)", r"python\g<major>.\g<minor>", e
            ),
        )
        for e in coverage_environments
    ]
    coverage_paths = lines(coveragerc()["paths"]["source"])
    assert coverage_paths == tox_paths


def test_coverage_environment_runs_at_the_end():
    """Coverage report runs after all environments collecting coverage."""
    coverage_depends = [
        e
        for p in tox_split_envlist(tox_ini()["testenv:coverage"]["depends"])
        for e in tox_expand_names(p)
    ]
    runs_coverage = [
        env
        for env, commands in tox_config_values("commands")
        if "coverage run" in commands
    ]
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
    assert "poetry.lock" not in git_files()


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
    tox_ini = open("tox.ini").read()
    offsets = [
        (re.search(fr"[testenv:(\w*,)?{e}(\w*,)?]", tox_ini).start(), e)
        for e in tox_envlist()
    ]
    assert offsets == sorted(offsets, key=lambda key: key[0])


def test_tox_deps_are_ordered():
    """Dependencies of tox environments should be in order."""
    for deps in tox_config_values("deps"):
        deps = lines(deps.value)
        ordered = sorted(deps, key=lambda key: key.lower())
        assert deps == ordered


def test_packages_are_ordered():
    """Packages of pyproject.toml files should be in order."""
    packages = [p["include"] for p in pyproject_toml()["tool"]["poetry"]["packages"]]
    assert packages == sorted(packages)


def test_build_requires_are_ordered():
    """Build system requirements of pyproject.toml files should be in order."""
    requires = pyproject_toml()["build-system"]["requires"]
    assert requires == sorted(requires)


def test_flake8_per_file_ignores_are_ordered():
    """Flake8 per file ignores should be in order."""
    per_file_ignores = [
        l.strip()
        for l in lines(flake8()["flake8"]["per-file-ignores"])
        if not l.startswith("#")
    ]
    assert per_file_ignores == sorted(per_file_ignores)


def test_flake8_ignored_errors_are_ordered():
    """Flake8 ignored error codes should be in order."""
    ignore = flake8()["flake8"]["ignore"].strip().split(", ")
    assert ignore == sorted(ignore)


def test_yamllint_ignored_patterns_are_ordered():
    """Yamllint ignored directory patterns should be in order."""
    ignore = lines(yamllint()["ignore"])
    assert ignore == sorted(ignore)


# Additional dependencies.


def test_poetry_avoid_additional_dependencies():
    """Python package should not have any of additional dependencies."""
    deps = list(pyproject_toml()["tool"]["poetry"]["dependencies"])
    assert deps == ["python"]


def test_pre_commit_hooks_avoid_additional_dependencies():
    """Additional dependencies of the pre-commit should not be used."""
    hooks = (hook for repo in pre_commit_yaml()["repos"] for hook in repo["hooks"])
    assert all("additional_dependencies" not in hook for hook in hooks)


# Version pinning.


def test_tox_deps_not_pinned():
    """Dependencies of tox environments should not have versions."""
    for deps in tox_config_values("deps"):
        assert "=" not in deps.value


def test_build_requires_not_pinned():
    """Build requirements of pyproject.toml files should not have versions."""
    requires = pyproject_toml()["build-system"]["requires"]
    assert not any("=" in r for r in requires)


def test_pre_commit_hooks_not_pinned():
    """Hook revisions of the pre-commit should not have versions."""
    assert all(repo["rev"] == "master" for repo in pre_commit_yaml()["repos"])


# Utils.


def tox_envlist():
    """List tox environments using CLI tool."""
    return [
        e
        for p in tox_split_envlist(tox_ini()["tox"]["envlist"])
        for e in tox_expand_names(p)
    ]


def tox_split_envlist(string):
    """Split envlist config string into list of strings.

    This function will respect generative environments.

    >>> tox_split_envlist('py{36,37},doctest,flake8')
    ['py{36,37}', 'doctest', 'flake8']

    """
    escaped = string
    while re.search(r"({[^,}]*),", escaped):
        escaped = re.subn(r"({[^,}]*),", r"\1:", escaped)[0]
    parts = escaped.split(",")
    return [re.subn(r":", ",", p)[0].strip() for p in parts]


def tox_expand_names(string):
    """Expand environment name to list of environments.

    >>> list(tox_expand_names('py{37,38}'))
    ['py37', 'py38']

    >>> list(tox_expand_names('doctest'))
    ['doctest']

    """
    # It's an incomplete implementation and works with current config only.
    if "{" not in string:
        yield string
    else:
        parts = re.split(r"{|}", string)
        index = [i for i, p in enumerate(parts) if "," in p][0]
        subs = parts[index].split(",")
        for s in subs:
            yield "".join(parts[:index] + [s])


def tox_config_environments():
    """List tox environments defined in the INI file."""
    return [
        e
        for k in tox_ini()
        for e in tox_expand_names(tox_section_name(k))
        if k not in {"tox", "DEFAULT"}
    ]


def tox_section_name(string):
    """Convert config section name to the tox environment name."""
    return re.sub(r"^testenv:", "", string)


Variable = collections.namedtuple("Variable", ("env", "value"))


def tox_config_values(variable):
    """Get variable value from all sections in the tox.ini file."""
    ini_parser = tox_ini()
    for section in ini_parser:
        if variable in ini_parser[section]:
            value = text(ini_parser[section][variable])
            for env in tox_expand_names(tox_section_name(section)):
                yield Variable(env, value)


def text(value):
    """Get text value from the INI file."""
    return textwrap.dedent(value.strip())


def lines(value):
    """Get lines of the multiline text from the INI file."""
    return text(value).splitlines()


def git_files():
    """List committed files."""
    return subprocess.check_output(["git", "ls-files"]).decode().splitlines()


# Config files.


def tox_ini():
    """Parse tox.ini file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    return ini_parser


def coveragerc():
    """Parse .coveragerc file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".coveragerc")
    return ini_parser


def flake8():
    """Parse .flake8 file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".flake8")
    return ini_parser


def yamllint():
    """Parse .yamllint file."""
    return yaml.safe_load(open(".yamllint").read())


def pre_commit_yaml():
    """Parse .pre-commit-config.yaml file."""
    return yaml.safe_load(open(".pre-commit-config.yaml").read())


def pyenv_versions():
    """Parse .python-version file."""
    return [v.split(".")[0:2] for v in open(".python-version").read().splitlines()]


def pyproject_toml():
    """Parse pyproject.toml file."""
    return tomlkit.loads(open("pyproject.toml").read())
