import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest
from mongoengine import (
    BooleanField,
    DateField,
    DateTimeField,
    DecimalField,
    DictField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    FloatField,
    GenericReferenceField,
    IntField,
    LazyReferenceField,
    ListField,
    LongField,
    MapField,
    ObjectIdField,
    StringField,
    URLField,
    UUIDField,
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


class BotDialog(Document):
    """
    BotDialog reproduces the field setup reported in issue #22, where a `StringField` with `choices` could be filled with a value outside the allowed list.

    Attributes:
        title (StringField): The dialog title. This field is required.
        status (StringField): The dialog status. This field is required.
        node_type (StringField): The node type, restricted to a fixed set of choices.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    title = StringField(required=True)
    status = StringField(required=True, default="NEW")
    node_type = StringField(default="standard", required=True, choices=["standard", "manual", "slot", "soft"])

    meta = {"collection": "test_documents"}


class Priority(Document):
    """
    Priority exercises `choices` declared as a list of (value, label) tuples on a non-string field, to ensure the choice extraction is type-agnostic.

    Attributes:
        level (IntField): The priority level, restricted to a fixed set of choices.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    level = IntField(required=True, choices=[(1, "Low"), (2, "Medium"), (3, "High")])

    meta = {"collection": "test_documents"}


class TypedListDocument(Document):
    """
    TypedListDocument exercises `ListField` mock generation across typed and untyped inner fields (issue #45).

    Attributes:
        numbers (ListField): A list of integers, typed via `ListField(IntField())`.
        names (ListField): A list of strings, typed via `ListField(StringField())`.
        tags (ListField): An untyped list, declared as plain `ListField()`.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    numbers = ListField(IntField(), required=True)
    names = ListField(StringField(), required=True)
    tags = ListField(required=True)

    meta = {"collection": "test_documents"}


class MiscFieldsDocument(Document):
    """
    MiscFieldsDocument exercises the field types that had no mock generator at all (issue #46).

    Attributes:
        birthday (DateField): Used to test `mock_DateField`.
        balance (DecimalField): Used to test `mock_DecimalField`.
        email (EmailField): Used to test `mock_EmailField`.
        homepage (URLField): Used to test `mock_URLField`.
        external_id (UUIDField): Used to test `mock_UUIDField`.
        views (LongField): Used to test `mock_LongField`.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    birthday = DateField(required=True)
    balance = DecimalField(required=True)
    email = EmailField(required=True)
    homepage = URLField(required=True)
    external_id = UUIDField(required=True, binary=False)
    views = LongField(required=True)

    meta = {"collection": "test_documents"}


class EmbeddedListDocument(Document):
    """
    EmbeddedListDocument exercises `EmbeddedDocumentListField` mock generation (issue #46).

    Attributes:
        departments (EmbeddedDocumentListField): A list of embedded `Department` documents.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    departments = EmbeddedDocumentListField(Department, required=True)

    meta = {"collection": "test_documents"}


class MapFieldDocument(Document):
    """
    MapFieldDocument exercises `MapField` mock generation across a typed inner field (issue #46).

    Attributes:
        scores (MapField): A mapping of names to integers, typed via `MapField(IntField())`.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    scores = MapField(IntField(), required=True)

    meta = {"collection": "test_documents"}


class ReferencedDocument(Document):
    """
    ReferencedDocument is the target document type for `LazyRefDocument` (issue #46).

    Attributes:
        name (StringField): A simple required field, only used to make the document saveable.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    name = StringField(required=True)

    meta = {"collection": "test_documents"}


class LazyRefDocument(Document):
    """
    LazyRefDocument exercises `LazyReferenceField` mock generation (issue #46).

    Attributes:
        ref (LazyReferenceField): A lazy reference to a `ReferencedDocument`.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    ref = LazyReferenceField(ReferencedDocument, required=True)

    meta = {"collection": "test_documents"}


class GenericRefDocument(Document):
    """
    GenericRefDocument exercises the `GenericReferenceField` limitation documented in issue #46.

    Attributes:
        ref (GenericReferenceField): A reference with no fixed `document_type`, which baker
            cannot mock automatically.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    ref = GenericReferenceField(required=True)

    meta = {"collection": "test_documents"}


class SequenceDocument(Document):
    """
    SequenceDocument exercises `baker.seq()` across the field types it supports: str, int, float, date and datetime.

    All fields are optional so each test can focus on the field passed as a `seq` kwarg without triggering
    random mock data on the others.

    Attributes:
        name (StringField): Used to test string sequences.
        age (IntField): Used to test int sequences.
        height_ft (FloatField): Used to test float sequences.
        birthday (DateField): Used to test date sequences.
        joined_at (DateTimeField): Used to test datetime sequences.

    Meta:
        collection (str): The name of the MongoDB collection where the documents are stored.
    """

    name = StringField(required=False)
    age = IntField(required=False)
    height_ft = FloatField(required=False)
    birthday = DateField(required=False)
    joined_at = DateTimeField(required=False)

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


def test_make_embedded_document_single_instance():
    """
    Test that `baker.make` returns a single `EmbeddedDocument` instance when `_quantity` is left at its default.

    Asserts:
        - The returned value is a `Department` instance, not a list.
    """
    instance = baker.make(Department)
    assert isinstance(instance, Department)


def test_make_embedded_document_respects_quantity():
    """
    Test that `baker.make` honors `_quantity` for `EmbeddedDocument` subclasses (issue #44).

    Previously the method returned after the first iteration for `EmbeddedDocument`,
    silently ignoring `_quantity` and always producing a single instance.

    Asserts:
        - The number of instances created equals the specified quantity (3).
        - Every created instance is a `Department`.
    """
    instances = baker.make(Department, _quantity=3)
    assert len(instances) == 3
    assert all(isinstance(instance, Department) for instance in instances)


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


def test_make_respects_string_field_choices():
    """
    Test that `baker.make` only fills a `StringField` with `choices` using an allowed value.

    This reproduces the scenario from issue #22, where `node_type` could be filled with a
    random string outside `choices`, causing a `ValidationError` on save.

    Asserts:
    - `node_type` is one of the values declared in `choices`.
    """
    instance = baker.make(BotDialog)
    assert instance.node_type in ["standard", "manual", "slot", "soft"]


def test_make_respects_tuple_choices_on_non_string_field():
    """
    Test that `baker.make` handles `choices` declared as (value, label) tuples on a non-string field.

    Asserts:
    - `level` is one of the values (not the labels) declared in `choices`.
    """
    instance = baker.make(Priority)
    assert instance.level in [1, 2, 3]


def test_make_respects_typed_list_field_inner_type():
    """
    Test that `baker.make` generates values matching the inner field type declared for a typed `ListField` (issue #45).

    Previously `mock_ListField` always generated a list of Faker words regardless of `field.field`,
    which broke mongoengine's validation for typed lists like `ListField(IntField())`.

    Asserts:
    - Every generated element of `numbers` is an `int`.
    """
    instance = baker.make(TypedListDocument)
    assert all(isinstance(value, int) for value in instance.numbers)


def test_make_untyped_list_field_falls_back_to_words():
    """
    Test that `baker.make` keeps generating a list of Faker words for an untyped `ListField` (`field.field is None`).

    Asserts:
    - `tags` is a list of 2 strings, preserving the pre-issue-#45 fallback behavior.
    """
    instance = baker.make(TypedListDocument)
    assert len(instance.tags) == 2
    assert all(isinstance(value, str) for value in instance.tags)


def test_make_typed_string_list_field_does_not_raise():
    """
    Test that `baker.make` does not raise when the inner field of a `ListField` is a `StringField` (issue #45).

    The inner field of a `ListField` is never bound to a document attribute, so its `.name` is `None`.
    `mock_StringField` used to call `hasattr(faker, field.name)` unconditionally, which raises
    `TypeError` for `None` once `mock_ListField` starts delegating to it.

    Asserts:
    - Every generated element of `names` is a `str`.
    """
    instance = baker.make(TypedListDocument)
    assert all(isinstance(value, str) for value in instance.names)


def test_make_generates_values_for_previously_unsupported_field_types():
    """
    Test that `baker.make` generates valid values for field types that previously had no generator (issue #46).

    Before this fix, `DateField`, `DecimalField`, `EmailField`, `URLField`, `UUIDField` and `LongField`
    all fell through to `_mock_default` and raised `ValueError: No mock defined for field type: ...`.

    Asserts:
    - `birthday` is a `date`.
    - `balance` is a `Decimal`.
    - `email` contains an "@".
    - `homepage` starts with "http".
    - `external_id` is a valid UUID.
    - `views` is an `int`.
    """
    instance = baker.make(MiscFieldsDocument)
    assert isinstance(instance.birthday, date)
    assert isinstance(instance.balance, Decimal)
    assert "@" in instance.email
    assert instance.homepage.startswith("http")
    assert uuid.UUID(str(instance.external_id))
    assert isinstance(instance.views, int)


def test_make_respects_embedded_document_list_field_inner_type():
    """
    Test that `baker.make` generates a list of embedded document instances for `EmbeddedDocumentListField` (issue #46).

    Asserts:
    - `departments` has 2 entries.
    - Every entry is a `Department` instance.
    """
    instance = baker.make(EmbeddedListDocument)
    assert len(instance.departments) == 2
    assert all(isinstance(department, Department) for department in instance.departments)


def test_make_respects_map_field_inner_type():
    """
    Test that `baker.make` generates a dict whose values match the inner field type declared for `MapField` (issue #46).

    Asserts:
    - `scores` has 2 entries.
    - Every value in `scores` is an `int`.
    """
    instance = baker.make(MapFieldDocument)
    assert len(instance.scores) == 2
    assert all(isinstance(value, int) for value in instance.scores.values())


def test_make_generates_instance_for_lazy_reference_field():
    """
    Test that `baker.make` generates a referenced document instance for `LazyReferenceField` (issue #46).

    Asserts:
    - `ref` resolves to a `ReferencedDocument` instance via `.fetch()`, mirroring `ReferenceField` support.
    """
    instance = baker.make(LazyRefDocument)
    assert isinstance(instance.ref.fetch(), ReferencedDocument)


def test_make_raises_clear_error_for_generic_reference_field():
    """
    Test that `baker.make` raises a clear, actionable error for `GenericReferenceField` (issue #46).

    `GenericReferenceField` has no fixed `document_type`, so baker has no way to know which
    Document subclass to instantiate automatically. This must raise a message distinct from the
    generic `_mock_default` fallback, so the caller understands *why* it can't be mocked.

    Asserts:
    - A `ValueError` mentioning the missing `document_type` is raised.
    """
    with pytest.raises(ValueError, match="no fixed document_type"):
        baker.make(GenericRefDocument)


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


def test_baker_has_seq_method():
    """Test to ensure that the `baker` object has a `seq` method and that it is callable."""
    assert hasattr(baker, "seq") and callable(baker.seq)


def test_seq_generates_incrementing_string_values():
    """
    Test that `baker.seq()` appends an incrementing counter to a string base value for each instance created.

    This reproduces the first example from issue #25, where a sequential field should produce
    'Test1', 'Test2', 'Test3' for three created instances.

    Asserts:
    - Each instance's `name` matches the base string with an increasing suffix, starting at 1.
    """
    instances = baker.make(SequenceDocument, name=baker.seq("Test"), _quantity=3)
    assert [instance.name for instance in instances] == ["Test1", "Test2", "Test3"]


def test_seq_respects_custom_start_and_increment_by_for_strings():
    """
    Test that `baker.seq()` honors custom `start` and `increment_by` values for string sequences.

    Asserts:
    - The counter starts at `start` and grows by `increment_by` on each subsequent instance.
    """
    instances = baker.make(SequenceDocument, name=baker.seq("Custom num: ", start=5, increment_by=2), _quantity=2)
    assert [instance.name for instance in instances] == ["Custom num: 5", "Custom num: 7"]


def test_seq_generates_incrementing_int_values():
    """
    Test that `baker.seq()` accumulates `increment_by` on top of an int base value for each instance created.

    Asserts:
    - The first instance's value is `value + increment_by`, and each following instance adds another
      `increment_by` on top of the previous one.
    """
    instances = baker.make(SequenceDocument, age=baker.seq(15, increment_by=3), _quantity=2)
    assert [instance.age for instance in instances] == [18, 21]


def test_seq_uses_default_increment_by_one():
    """
    Test that `baker.seq()` defaults `increment_by` to 1 when not provided.

    Asserts:
    - Consecutive instances increase by exactly 1 from the base int value.
    """
    instances = baker.make(SequenceDocument, age=baker.seq(10), _quantity=3)
    assert [instance.age for instance in instances] == [11, 12, 13]


def test_seq_generates_incrementing_float_values():
    """
    Test that `baker.seq()` accumulates `increment_by` on top of a float base value for each instance created.

    Asserts:
    - The first instance's value is `value + increment_by`, and each following instance adds another
      `increment_by` on top of the previous one.
    """
    instances = baker.make(SequenceDocument, height_ft=baker.seq(5.5, increment_by=0.25), _quantity=2)
    assert [instance.height_ft for instance in instances] == [5.75, 6.0]


def test_seq_generates_incrementing_date_values():
    """
    Test that `baker.seq()` accumulates a `timedelta` `increment_by` on top of a `date` base value.

    Asserts:
    - Each instance's `birthday` advances by one `increment_by` step from the previous instance.
    """
    instances = baker.make(
        SequenceDocument, birthday=baker.seq(date(2014, 7, 21), increment_by=timedelta(days=1)), _quantity=2
    )
    assert [instance.birthday for instance in instances] == [date(2014, 7, 22), date(2014, 7, 23)]


def test_seq_generates_incrementing_datetime_values():
    """
    Test that `baker.seq()` accumulates a `timedelta` `increment_by` on top of a `datetime` base value.

    Asserts:
    - Each instance's `joined_at` advances by one `increment_by` step from the previous instance.
    """
    base_datetime = datetime(2025, 3, 13, 9, 0, 0)
    instances = baker.make(
        SequenceDocument, joined_at=baker.seq(base_datetime, increment_by=timedelta(days=1)), _quantity=3
    )
    assert [instance.joined_at for instance in instances] == [
        datetime(2025, 3, 14, 9, 0, 0),
        datetime(2025, 3, 15, 9, 0, 0),
        datetime(2025, 3, 16, 9, 0, 0),
    ]


def test_seq_with_quantity_one_returns_single_incremented_value():
    """
    Test that `baker.seq()` works when `_quantity` is left at its default of 1.

    Asserts:
    - The single created instance receives the first value of the sequence.
    """
    instance = baker.make(SequenceDocument, name=baker.seq("Solo"))
    assert instance.name == "Solo1"


def test_seq_only_applies_to_the_field_it_is_assigned_to():
    """
    Test that a `seq` value passed for one field does not affect a plain value passed for another field.

    Asserts:
    - The sequential field varies across instances while the plain field stays constant.
    """
    instances = baker.make(SequenceDocument, name=baker.seq("Test"), age=42, _quantity=3)
    assert [instance.name for instance in instances] == ["Test1", "Test2", "Test3"]
    assert [instance.age for instance in instances] == [42, 42, 42]


def test_seq_raises_for_unsupported_value_type():
    """
    Test that `baker.seq()` raises a `ValueError` when used with a value type it doesn't know how to increment.

    Asserts:
    - A `ValueError` mentioning the unsupported type is raised when the sequence is resolved.
    """
    with pytest.raises(ValueError, match="No sequence strategy defined for value type: list"):
        baker.make(SequenceDocument, name=baker.seq([1, 2, 3]), _quantity=2)
