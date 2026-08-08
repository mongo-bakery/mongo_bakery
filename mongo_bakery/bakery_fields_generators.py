from bson import ObjectId
from faker import Faker

faker = Faker()


def mock_DateField(field):
    return faker.date_this_decade()


def mock_DecimalField(field):
    return faker.pydecimal(left_digits=5, right_digits=field.precision, positive=True)


def mock_EmailField(field):
    return faker.email()


def mock_URLField(field):
    return faker.url()


def mock_UUIDField(field):
    return faker.uuid4()


def mock_StringField(field):
    value = faker.word()
    if field.name and hasattr(faker, field.name):
        value = getattr(faker, field.name)()
    return value


def mock_IntField(field):
    return faker.random_int(min=0, max=100)


mock_LongField = mock_IntField


def mock_FloatField(field):
    return faker.pyfloat(min_value=0.1, max_value=1000)


def mock_BooleanField(field):
    return faker.boolean()


def mock_DateTimeField(field):
    return faker.date_time_this_decade()


def mock_ListField(field, baker):
    if field.field is None:
        return [faker.word() for _ in range(2)]
    return [baker._generate_mock_data(field.field) for _ in range(2)]


def mock_EmbeddedDocumentListField(field, baker):
    return mock_ListField(field, baker)


def mock_DictField(field):
    return {"key": faker.word(), "value": faker.word()}


def mock_MapField(field, baker):
    return {faker.word(): baker._generate_mock_data(field.field) for _ in range(2)}


def mock_ObjectIdField(field):
    return ObjectId()


def mock_EmbeddedDocumentField(field, baker):
    return baker.make(field.document_type)


def mock_ReferenceField(field, baker):
    return baker.make(field.document_type)


def mock_LazyReferenceField(field, baker):
    return baker.make(field.document_type)


def mock_GenericReferenceField(field, baker):
    raise ValueError(
        "GenericReferenceField has no fixed document_type to mock automatically; "
        "pass an explicit value via baker.make(..., <field_name>=<document_instance>)."
    )
