from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ListField,
    ObjectIdField,
    StringField,
)

from mongo_bakery import baker


class Department(EmbeddedDocument):
    name = StringField(required=True)
    location = StringField(required=True)


class TestDocument(Document):
    _id = ObjectIdField(primary_key=True)
    name = StringField(required=True)
    age = IntField(required=True)
    salary = FloatField(required=True)
    is_admin = BooleanField(required=True)
    birthday = DateTimeField(required=True)
    dependents = ListField(StringField(), required=True)
    permissions = DictField(required=True)
    department = EmbeddedDocumentField("Department", required=True)

    meta = {"collection": "test_documents"}


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


def test_make_single_instance():
    instance = baker.make(TestDocument)
    assert isinstance(instance, TestDocument)


def test_make_multiple_instances():
    instances = baker.make(TestDocument, _quantity=3)
    assert len(instances) == 3


def test_cleanup():
    instance = baker.make(TestDocument)  # noqa F841
    baker.cleanup()
    assert TestDocument.objects.count() == 0
