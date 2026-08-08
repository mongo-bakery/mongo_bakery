import pytest

from mongo_bakery import baker
from mongo_bakery.pytest_plugin import baker as baker_fixture
from tests.test_mongo_bakery_basics import DocumentToTest


def test_baker_fixture_yields_the_shared_baker_instance():
    """
    Test that the `baker` pytest fixture yields the shared `mongo_bakery` baker instance (issue #53).

    Drives the fixture's underlying generator function directly (via `__wrapped__`, the attribute
    `@pytest.fixture` preserves pointing at the raw function) the same way pytest itself would,
    without needing a full nested pytest run.

    Asserts:
    - The first value produced by the generator is the shared `baker` instance.
    - The generator has exactly one more step (the teardown), matching a `@pytest.fixture` with a
      single `yield`.
    """
    generator = baker_fixture.__wrapped__()
    yielded = next(generator)
    assert yielded is baker
    with pytest.raises(StopIteration):
        next(generator)


def test_baker_fixture_cleans_up_created_instances_on_teardown():
    """
    Test that the `baker` pytest fixture calls `cleanup()` automatically after the test (issue #53).

    Drives the fixture's underlying generator function directly, creating a `DocumentToTest`
    instance through the yielded `baker` and then advancing the generator past its `yield` to
    trigger the teardown, mirroring what pytest does when a test using this fixture finishes.

    Asserts:
    - Before teardown, the created instance exists in the database.
    - After teardown, `cleanup()` has deleted it.
    """
    generator = baker_fixture.__wrapped__()
    yielded_baker = next(generator)
    yielded_baker.make(DocumentToTest)
    assert DocumentToTest.objects.count() == 1

    with pytest.raises(StopIteration):
        next(generator)
    assert DocumentToTest.objects.count() == 0
