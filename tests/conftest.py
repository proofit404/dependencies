def pytest_collection_modifyitems(session, config, items):
    """
    Do not run actual tests in linter environments.
    """
    for linter in ["flake8", "mypy", "black", "isort"]:
        try:
            if config.getoption("--" + linter):
                items[:] = [item for item in items if item.get_closest_marker(linter)]
        except ValueError:
            # An old python version without installed linter.
            pass
