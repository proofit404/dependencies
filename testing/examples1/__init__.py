import pytest


# Fixtures.


@pytest.fixture()
def e():
    """Fixture with all possible definitions."""
    import examples1.definitions

    return examples1.definitions
