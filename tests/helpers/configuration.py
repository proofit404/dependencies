import collections
import configparser
import datetime
import itertools
import re
import subprocess
import textwrap

import tomlkit
import yaml


def _azure_release_use_max_base_python():
    version = max(sorted(f"{major}.{minor}" for major, minor in _pyenv_versions()))
    installed = _azure_pipelines("jobs", 1, "steps", 0, "inputs", "versionSpec")
    assert version == installed


def _tox_environments_use_all_pyenv_versions():
    versions = [f"py{major}{minor}" for major, minor in _pyenv_versions()]
    for version in versions:
        assert version in _tox_envlist()


def _tox_environments_use_max_base_python():
    version = max(
        sorted(f"python{major}.{minor}" for major, minor in _pyenv_versions())
    )
    for basepython in _tox_config_values("basepython"):
        assert basepython.value == version


def _tox_envlist_contains_all_tox_environments():
    assert _tox_envlist() == _tox_config_environments()


def _tox_no_default_environment():
    assert "testenv" not in _tox_ini()


def _tox_no_factor_environments():
    assert not any("-" in e for e in _tox_envlist())


def _tox_no_factor_deps():
    for deps in _tox_config_values("deps"):
        for dep in _lines(deps.value):
            assert ":" not in dep


def _tox_single_line_settings_are_written_same_line():
    for section in _tox_ini().values():
        for setting in _Settings()._singleline():
            value = section.get(setting)
            if value is not None:
                assert not value.startswith("\n")


def _tox_multiline_settings_are_written_next_line():
    for section in _tox_ini().values():
        for setting in _Settings()._multiline():
            value = section.get(setting)
            if value is not None:
                assert value.startswith("\n") or not value


def _tox_no_unknown_settings():
    for section in _tox_ini().values():
        for setting in section:
            assert setting in _Settings()._known()


def _coverage_include_all_packages():
    coverage_sources = _coveragerc()["run"]["source"].strip().splitlines()

    packages = set()
    helpers = set()

    for f in _git_files():
        parts = [re.sub(r"\.py$", "", p) for p in f.split("/")]
        if len(parts) > 1 and parts[0] == "src":
            packages.add(parts[1])
        if len(parts) > 2 and parts[0] == "tests" and parts[1] == "helpers":
            helpers.add(parts[2])

    assert coverage_sources == sorted(packages) + sorted(helpers) + ["tests"]


def _coverage_environment_runs_at_the_end():
    coverage_depends = [
        e
        for p in _tox_split_envlist(_tox_ini()["testenv:coverage"]["depends"])
        for e in _tox_expand_names(p)
    ]
    runs_coverage = [
        env
        for env, commands in _tox_config_values("commands")
        if "coverage run" in commands
    ]
    assert coverage_depends == runs_coverage


def _poetry_python_version_use_all_pyenv_versions():
    pyenv_version = " || ".join(
        f"~{major}.{minor}" for major, minor in _pyenv_versions()
    )
    poetry_version = _pyproject_toml()["tool"]["poetry"]["dependencies"]["python"]
    assert pyenv_version == poetry_version


def _ini_files_indentation():
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


def _ini_files_boolean_case():
    ini_files = [_tox_ini, _coveragerc, _flake8, _importlinter, _pytest_ini]
    sections = itertools.chain.from_iterable(ini().values() for ini in ini_files)
    values = itertools.chain.from_iterable(section.values() for section in sections)
    for value in values:
        if value.lower() in {"true", "false"}:
            assert value == value.lower()


def _lock_files_not_committed():
    assert "poetry.lock" not in _git_files()


def _license_year():
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


def _tox_environments_are_ordered():
    tox_ini = open("tox.ini").read()
    offsets = [
        (re.search(fr"[testenv:(\w*,)?{e}(\w*,)?]", tox_ini).start(), e)
        for e in _tox_envlist()
    ]
    assert offsets == sorted(offsets, key=lambda key: key[0])


def _tox_settings_are_ordered():
    tox_ini = open("tox.ini").read()
    sections = []
    for l in _lines(tox_ini):
        if l.startswith("["):
            section = []
            sections.append(section)
        elif re.match(r"\S", l):
            section.append(l.split("=")[0].strip())
    for section in sections:
        ordered = _Settings()._sort(section)
        assert section == ordered


def _tox_deps_are_ordered():
    for deps in _tox_config_values("deps"):
        deps = _lines(deps.value)
        ordered = sorted(deps, key=lambda key: key.lower())
        assert deps == ordered


def _tox_whitelist_externals_are_ordered():
    for externals in _tox_config_values("whitelist_externals"):
        externals = _lines(externals.value)
        assert externals == sorted(externals)


def _packages_are_ordered():
    packages = [p["include"] for p in _pyproject_toml()["tool"]["poetry"]["packages"]]
    assert packages == sorted(packages)


def _build_requires_are_ordered():
    requires = _pyproject_toml()["build-system"]["requires"]
    assert requires == sorted(requires)


def _flake8_per_file_ignores_are_ordered():
    per_file_ignores = [
        l.strip()
        for l in _lines(_flake8()["flake8"]["per-file-ignores"])
        if not l.startswith("#")
    ]
    assert per_file_ignores == sorted(per_file_ignores)


def _flake8_ignored_errors_are_ordered():
    ignore = _flake8()["flake8"]["ignore"].strip().split(", ")
    assert ignore == sorted(ignore)


def _yamllint_ignored_patterns_are_ordered():
    ignore = _lines(_yamllint()["ignore"])
    assert ignore == sorted(ignore)


def _poetry_avoid_additional_dependencies():
    deps = list(_pyproject_toml()["tool"]["poetry"]["dependencies"])
    assert deps == ["python"]


def _pre_commit_hooks_avoid_additional_dependencies():
    hooks = (hook for repo in _pre_commit_yaml()["repos"] for hook in repo["hooks"])
    assert all("additional_dependencies" not in hook for hook in hooks)


def _tox_deps_not_pinned():
    for deps in _tox_config_values("deps"):
        assert "=" not in deps.value


def _build_requires_not_pinned():
    requires = _pyproject_toml()["build-system"]["requires"]
    assert not any("=" in r for r in requires)


def _pre_commit_hooks_not_pinned():
    assert all(repo["rev"] == "master" for repo in _pre_commit_yaml()["repos"])


class _Settings:
    class _Text:
        is_text = True

    class _String:
        is_text = False

    class _Boolean:
        is_text = False

    keys = [
        ("envlist", _Text),
        ("isolated_build", _Boolean),
        ("basepython", _String),
        ("skip_install", _Boolean),
        ("ignore_outcome", _Boolean),
        ("install_command", _String),
        ("setenv", _Text),
        ("deps", _Text),
        ("commands", _Text),
        ("depends", _Text),
        ("whitelist_externals", _Text),
    ]

    def _known(self):
        return [s[0] for s in self.keys]

    def _singleline(self):
        for name, kind in self.keys:
            if not kind.is_text:
                yield name

    def _multiline(self):
        for name, kind in self.keys:
            if kind.is_text:
                yield name

    def _sort(self, section):
        keys = [k[0] for k in self.keys]
        offsets = [(keys.index(k), k) for k in section]
        return [e[1] for e in sorted(offsets, key=lambda e: e[0])]


def _tox_envlist():
    return [
        e
        for p in _tox_split_envlist(_tox_ini()["tox"]["envlist"])
        for e in _tox_expand_names(p)
    ]


def _tox_split_envlist(string):
    # => tox_split_envlist('py{36,37},doctest,flake8')
    # -> ['py{36,37}', 'doctest', 'flake8']
    escaped = string
    while re.search(r"({[^,}]*),", escaped):
        escaped = re.subn(r"({[^,}]*),", r"\1:", escaped)[0]
    parts = escaped.split(",")
    return [re.subn(r":", ",", p)[0].strip() for p in parts]


def _tox_expand_names(string):
    # => list(_tox_expand_names('py{37,38}'))
    # -> ['py37', 'py38']
    # => list(_tox_expand_names('doctest'))
    # -> ['doctest']
    if "{" not in string:
        yield string
    else:
        parts = re.split(r"{|}", string)
        index = [i for i, p in enumerate(parts) if "," in p][0]
        subs = parts[index].split(",")
        for s in subs:
            yield "".join(parts[:index] + [s])


def _tox_config_environments():
    return [
        e
        for k in _tox_ini()
        for e in _tox_expand_names(_tox_section_name(k))
        if k not in {"tox", "DEFAULT"}
    ]


def _tox_section_name(string):
    return re.sub(r"^testenv:", "", string)


Variable = collections.namedtuple("Variable", ("env", "value"))


def _tox_config_values(variable):
    ini_parser = _tox_ini()
    for section in ini_parser:
        if variable in ini_parser[section]:
            value = _text(ini_parser[section][variable])
            for env in _tox_expand_names(_tox_section_name(section)):
                yield Variable(env, value)


def _text(value):
    return textwrap.dedent(value.strip())


def _lines(value):
    return _text(value).splitlines()


def _git_files():
    return subprocess.check_output(["git", "ls-files"]).decode().splitlines()


def _azure_pipelines(*items):
    result = yaml.safe_load(open("azure-pipelines.yml").read())
    for item in items:
        result = result[item]
    return result


def _tox_ini():
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    return ini_parser


def _coveragerc():
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".coveragerc")
    return ini_parser


def _flake8():
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".flake8")
    return ini_parser


def _importlinter():
    ini_parser = configparser.ConfigParser()
    ini_parser.read(".importlinter")
    return ini_parser


def _pytest_ini():
    ini_parser = configparser.ConfigParser()
    ini_parser.read("pytest.ini")
    return ini_parser


def _yamllint():
    return yaml.safe_load(open(".yamllint").read())


def _pre_commit_yaml():
    return yaml.safe_load(open(".pre-commit-config.yaml").read())


def _pyenv_versions():
    return [v.split(".")[0:2] for v in open(".python-version").read().splitlines()]


def _pyproject_toml():
    return tomlkit.loads(open("pyproject.toml").read())


def _main():
    _azure_release_use_max_base_python()
    _tox_environments_use_all_pyenv_versions()
    _tox_environments_use_max_base_python()
    _tox_envlist_contains_all_tox_environments()
    _tox_no_default_environment()
    _tox_no_factor_environments()
    _tox_no_factor_deps()
    _tox_single_line_settings_are_written_same_line()
    _tox_multiline_settings_are_written_next_line()
    _tox_no_unknown_settings()
    _coverage_include_all_packages()
    _coverage_environment_runs_at_the_end()
    _poetry_python_version_use_all_pyenv_versions()
    _ini_files_indentation()
    _ini_files_boolean_case()
    _lock_files_not_committed()
    _license_year()
    _tox_environments_are_ordered()
    _tox_settings_are_ordered()
    _tox_deps_are_ordered()
    _tox_whitelist_externals_are_ordered()
    _packages_are_ordered()
    _build_requires_are_ordered()
    _flake8_per_file_ignores_are_ordered()
    _flake8_ignored_errors_are_ordered()
    _yamllint_ignored_patterns_are_ordered()
    _poetry_avoid_additional_dependencies()
    _pre_commit_hooks_avoid_additional_dependencies()
    _tox_deps_not_pinned()
    _build_requires_not_pinned()
    _pre_commit_hooks_not_pinned()


if __name__ == "__main__":  # pragma: no branch
    _main()
