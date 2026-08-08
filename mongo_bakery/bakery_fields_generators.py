from bson import ObjectId
from faker import Faker

faker = Faker()


def mock_StringField(field):
    value = faker.word()
    if hasattr(faker, field.name):
        value = getattr(faker, field.name)()
    return value


def mock_IntField(field):
    return faker.random_int(min=0, max=100)


def mock_FloatField(field):
    return faker.pyfloat(min_value=0.1, max_value=1000)


def mock_BooleanField(field):
    return faker.boolean()


def mock_DateTimeField(field):
    return faker.date_time_this_decade()


def mock_ListField(field):
    return [faker.word() for _ in range(2)]


def mock_DictField(field):
    return {"key": faker.word(), "value": faker.word()}


def mock_ObjectIdField(field):
    return ObjectId()


def mock_EmbeddedDocumentField(field, baker):
    return baker.make(field.document_type)


def mock_ReferenceField(field, baker):
    return baker.make(field.document_type)
