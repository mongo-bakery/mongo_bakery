import pytest

from mongo_bakery import baker as _baker


@pytest.fixture
def baker():
    """
    Yield the shared `mongo_bakery` baker and clean up any instances it created after the test.

    Registered as a pytest plugin (see the `pytest11` entry point in pyproject.toml), so this
    fixture is available in any project that has `mongo_bakery` installed, with no extra setup.

    Yields:
        Baker: The shared `mongo_bakery` baker instance.
    """
    yield _baker
    _baker.cleanup()
