import inspect
import sys
from contextlib import ExitStack
from typing import Any
from unittest.mock import MagicMock, patch

from bson import ObjectId
from faker import Faker
from mongoengine import Document, EmbeddedDocument, fields, signals

faker = Faker()


class Baker:
    def __init__(self, mock_class=None):
        self._dependencies_to_patch = mock_class or []
        self._created_instances = []

    def mock_dependencies(self, mock_class: list):
        """
        Mocks the specified dependencies for testing purposes.

        Args:
            mock_class (list): A list of classes or modules to be mocked.
        """
        self._dependencies_to_patch = mock_class

    def make(self, document_class: Document, _quantity: int = 1, **kwargs: dict[Any, Any]) -> Document:
        """
        Creates and saves one or more instances of a MongoEngine document.

        Args:
            document_class (Document): The MongoEngine document class to instantiate.
            _quantity (int, optional): The number of instances to create. Defaults to 1.
            **kwargs: Additional field values to set on the document instances.

        Returns:
            Document or list[Document]: A single document instance if _quantity is 1,
            otherwise a list of document instances.

        Raises:
            ValueError: If the provided document_class is not a subclass of mongoengine.Document
            or mongoengine.EmbeddedDocument.
        """
        """Creates and saves one or more instances of a MongoEngine document."""
        if not (issubclass(document_class, Document) or issubclass(document_class, EmbeddedDocument)):
            raise ValueError("The document must be a subclass of mongoengine.Document")

        patch_dependencies = {}
        module_name = document_class.__module__

        if module_name in sys.modules:
            module = sys.modules[module_name]
            source_lines = inspect.getsource(module).splitlines()
            for dep in self._dependencies_to_patch:
                if any(f" {dep}" in line or f"{dep} " in line for line in source_lines):
                    patch_dependencies[dep] = patch(f"{module_name}.{dep}", new=MagicMock())

        # Temporarily disable signals
        if hasattr(document_class, "post_save"):
            signals.post_save.disconnect(document_class.post_save, sender=document_class)

        instances = []
        with ExitStack() as stack:
            for mock in patch_dependencies.values():
                stack.enter_context(mock)

            for _ in range(_quantity):
                instance_data = {}
                for field_name, field in document_class._fields.items():
                    if field_name in kwargs or field_name == "id":
                        continue
                    if not field.required:
                        continue
                    instance_data[field_name] = self._generate_mock_data(field)

                instance_data.update(kwargs)
                instance = document_class(**instance_data)
                if issubclass(document_class, EmbeddedDocument):
                    instances.append(instance)
                    return instances[0]
                instance.save()
                self._created_instances.append(instance)
                instances.append(instance)

        # Reconnect the signal after creating the instances
        if hasattr(document_class, "post_save"):
            signals.post_save.connect(document_class.post_save, sender=document_class)

        return instances if _quantity > 1 else instances[0]

    def _generate_mock_data(self, field):
        """
        Generate mock data based on the provided field type.

        Args:
            field (Field): The field for which to generate mock data.

        Returns:
            Any: Mock data appropriate for the given field type.

        Raises:
            ValueError: If the field type is not supported.

        Supported field types:
            - StringField: Returns a random word.
            - IntField: Returns a random integer between 0 and 100.
            - FloatField: Returns a random float between 0.1 and 1000.
            - BooleanField: Returns a random boolean value.
            - DateTimeField: Returns a random datetime within the last decade.
            - ListField: Returns a list of two random words.
            - DictField: Returns a dictionary with random word values.
            - ObjectIdField: Returns a new ObjectId.
            - EmbeddedDocumentField: Returns a mock embedded document.
            - ReferenceField: Returns a mock reference document.
        """
        match field:
            case fields.StringField():
                value = faker.word()
                if hasattr(faker, field.name):
                    value = getattr(faker, field.name)()
                return value
            case fields.IntField():
                return faker.random_int(min=0, max=100)
            case fields.FloatField():
                return faker.pyfloat(min_value=0.1, max_value=1000)
            case fields.BooleanField():
                return faker.boolean()
            case fields.DateTimeField():
                return faker.date_time_this_decade()
            case fields.ListField():
                return [faker.word() for _ in range(2)]
            case fields.DictField():
                return {"key": faker.word(), "value": faker.word()}
            case fields.ObjectIdField():
                return ObjectId()
            case fields.EmbeddedDocumentField() | fields.ReferenceField():
                return self.make(field.document_type)

    def cleanup(self):
        """
        Delete all created instances.

        This method iterates over all instances stored in the `_created_instances`
        list, calls their `delete` method to remove them, and then clears the list.
        """
        for instance in self._created_instances:
            instance.delete()
        self._created_instances.clear()


baker = Baker()
