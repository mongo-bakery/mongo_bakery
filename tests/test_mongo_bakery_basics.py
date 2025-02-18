from mongoengine import Document

from mongo_bakery import baker


def test_mongo_bakery_module_exists():
    """Test to ensure that the 'baker' module from 'mongo_bakery' is imported correctly."""
    assert baker is not None


def test_baker_has_make_method():
    """Test to ensure that the 'baker' object has a 'make' method and that it is callable."""
    assert hasattr(baker, "make") and callable(baker.make)


def test_baker_make_accepts_document():
    """Test to ensure that the 'make' method of the 'baker' object accept a Mongo Document and return its instance."""
    class FakeDocument(Document):
        meta = {"collection": "fake_collection"}

    obj = baker.make(FakeDocument)

    assert isinstance(obj, FakeDocument)
