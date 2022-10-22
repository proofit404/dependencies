import pytest


# Fixtures.


@pytest.fixture()
def e():
    """Fixture with all possible definitions."""
    import examples.definitions

    return examples.definitions
