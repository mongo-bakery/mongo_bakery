import mongoengine
import mongomock
import pytest


@pytest.fixture(scope="session", autouse=True)
def mock_mongo_connection():
    mongoengine.connect(
        "testdb",
         host="mongodb://localhost",
         alias="default",
         mongo_client_class=mongomock.MongoClient,
         uuidRepresentation='standard')
