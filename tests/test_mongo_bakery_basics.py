from unittest.mock import patch

import pytest
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
    signals,
)

from mongo_bakery import baker


class Department(EmbeddedDocument):
    name = StringField(required=True)
    location = StringField(required=True)


class DocumentToTest(Document):
    _id = ObjectIdField(primary_key=True)
    name = StringField(required=True)
    age = IntField(required=True)
    salary = FloatField(required=True)
    is_admin = BooleanField(required=True)
    birthday = DateTimeField(required=True)
    dependents = ListField(StringField(), required=True)
    permissions = DictField(required=True)
    department = EmbeddedDocumentField("Department", required=True)
    region = StringField(required=False)

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
    instance = baker.make(DocumentToTest)
    assert isinstance(instance, DocumentToTest)


def test_make_multiple_instances():
    instances = baker.make(DocumentToTest, _quantity=3)
    assert len(instances) == 3


def test_cleanup():
    instance = baker.make(DocumentToTest)  # noqa F841
    baker.cleanup()
    assert DocumentToTest.objects.count() == 0


def test_mock_dependencies():
    baker.mock_dependencies(["SomeClass", "AnotherClass"])
    instance = baker.make(DocumentToTest)
    assert isinstance(instance, DocumentToTest)


def test_make_with_invalid_document_class():
    with pytest.raises(ValueError, match="The document must be a subclass of mongoengine.Document"):
        baker.make(str)


def test_signals_disconnected_and_reconnected():
    class DocumentWithSignals(Document):
        name = StringField(required=True)
        age = IntField(required=True)

        meta = {"collection": "test_documents"}

        @classmethod
        def post_save(cls, sender, document, **kwargs):
            pass

    with (
        patch.object(signals.post_save, "disconnect") as mock_disconnect,
        patch.object(signals.post_save, "connect") as mock_connect,
    ):
        baker.make(DocumentWithSignals)
        mock_connect.assert_called_once_with(DocumentWithSignals.post_save, sender=DocumentWithSignals)
        mock_disconnect.assert_called_once_with(DocumentWithSignals.post_save, sender=DocumentWithSignals)
