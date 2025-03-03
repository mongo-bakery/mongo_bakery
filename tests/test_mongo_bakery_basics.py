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
)

from mongo_bakery import baker


class Department(EmbeddedDocument):
    """
    Department class represents an embedded document in MongoDB.

    Attributes:
        name (str): The name of the department. This field is required.
        location (str): The location of the department. This field is required.
    """

    name = StringField(required=True)
    address = StringField(required=True)
    location = StringField(required=True)


class DocumentToTest(Document):
    """
    DocumentToTest is a MongoDB document model that represents a test document with various fields.

    Attributes:
        _id (ObjectIdField): The primary key for the document.
        name (StringField): The name of the individual. This field is required.
        age (IntField): The age of the individual. This field is required.
        salary (FloatField): The salary of the individual. This field is required.
        is_admin (BooleanField): Indicates if the individual is an admin. This field is required.
        birthday (DateTimeField): The birthday of the individual. This field is required.
        dependents (ListField): A list of dependents' names. This field is required.
        permissions (DictField): A dictionary of permissions. This field is required.
        department (EmbeddedDocumentField): The department information, embedded as a document. This field is required.
        region (StringField): The region of the individual. This field is optional.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    _id = ObjectIdField(primary_key=True)
    name = StringField(required=True)
    email = StringField(required=True)
    company = StringField(required=True)
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
    """
    Test to ensure that the `baker` module exists and is not None.

    This test checks if the `baker` module has been imported correctly and is available for use.
    """
    assert baker is not None


def test_baker_has_make_method():
    """
    Test to ensure that the 'baker' object has a 'make' method and that it is callable.

    This test checks if the 'baker' object has an attribute named 'make' and verifies
    that this attribute is a callable method.
    """
    assert hasattr(baker, "make") and callable(baker.make)


def test_baker_make_accepts_document():
    """
    Test that the `baker.make` method accepts a `Document` subclass and returns an instance of it.

    This test defines a `FakeDocument` class that subclasses `Document` and specifies a collection
    name in its `meta` attribute. It then uses `baker.make` to create an instance of `FakeDocument`
    and asserts that the created object is indeed an instance of `FakeDocument`.
    """

    class FakeDocument(Document):
        meta = {"collection": "fake_collection"}

    obj = baker.make(FakeDocument)

    assert isinstance(obj, FakeDocument)


def test_make_single_instance():
    """
    Test the creation of a single instance of DocumentToTest using baker.make.

    This test ensures that the baker.make method correctly creates an instance
    of the DocumentToTest class and verifies that the created instance is indeed
    an instance of DocumentToTest.

    Assertions:
        - The created instance is an instance of DocumentToTest.
    """
    instance = baker.make(DocumentToTest)
    assert isinstance(instance, DocumentToTest)


def test_make_multiple_instances():
    """
    Test that multiple instances of DocumentToTest can be created using the baker.make method.

    This test verifies that the baker.make method can create multiple instances of the
    DocumentToTest class when the _quantity parameter is specified.

    Assertions:
        - The number of instances created should be equal to the specified quantity (3).
    """
    instances = baker.make(DocumentToTest, _quantity=3)
    assert len(instances) == 3


def test_cleanup():
    """
    Test the cleanup functionality of the baker instance.

    This test creates an instance of `DocumentToTest` using the `baker.make` method,
    then calls `baker.cleanup` to remove all created instances. Finally, it asserts
    that the count of `DocumentToTest` objects is zero, ensuring that the cleanup
    process works correctly.
    """
    instance = baker.make(DocumentToTest)  # noqa F841
    baker.cleanup()
    assert DocumentToTest.objects.count() == 0


def test_mock_dependencies():
    """
    Test the mock_dependencies function of the baker module.

    This test ensures that the mock_dependencies function correctly mocks the specified dependencies
    and that an instance of DocumentToTest can be created using the baker.make function.

    Steps:
    1. Mock the dependencies "SomeClass" and "AnotherClass" using baker.mock_dependencies.
    2. Create an instance of DocumentToTest using baker.make.
    3. Assert that the created instance is indeed an instance of DocumentToTest.

    Asserts:
    - The created instance is an instance of DocumentToTest.
    """
    baker.mock_dependencies(["SomeClass", "AnotherClass"])
    instance = baker.make(DocumentToTest)
    assert isinstance(instance, DocumentToTest)


def test_make_with_invalid_document_class():
    """
    Test that `baker.make` raises a `ValueError` when called with an invalid document class.

    This test ensures that the `baker.make` function raises a `ValueError` with the appropriate
    error message when it is called with a class that is not a subclass of `mongoengine.Document`.

    Raises:
        ValueError: If the provided class is not a subclass of `mongoengine.Document`.
    """
    with pytest.raises(ValueError, match="The document must be a subclass of mongoengine.Document"):
        baker.make(str)
