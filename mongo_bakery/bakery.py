import inspect
import sys
from contextlib import ExitStack
from unittest.mock import MagicMock, patch

from bson import ObjectId
from faker import Faker
from mongoengine import Document, fields, signals

faker = Faker()


class Baker:
    def __init__(self, mock_class=[]):
        self._dependencies_to_patch = mock_class
        self._created_instances = []

    def mock_dependencies(self, mock_class: list):
        self._dependencies_to_patch = mock_class

    def make(self, document_class: Document, _quantity=1, **kwargs) -> Document:
        """Creates and saves one or more instances of a MongoEngine document."""
        if not issubclass(document_class, Document):
            raise ValueError("The document must be a subclass of mongoengine.Document")

        patch_dependencies = {}
        module_name = document_class.__module__

        if module_name in sys.modules:
            module = sys.modules[module_name]
            source_lines = inspect.getsource(module).splitlines()
            for dep in self._dependencies_to_patch:
                if any(f" {dep}" in line or f"{dep} " in line for line in source_lines):
                    patch_dependencies[dep] = patch(
                        f"{module_name}.{dep}", new=MagicMock()
                    )

        # Temporarily disable signals
        if hasattr(document_class, "post_save"):
            signals.post_save.disconnect(
                document_class.post_save, sender=document_class
            )

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
                instance.save()
                self._created_instances.append(instance)
                instances.append(instance)

        # Reconnect the signal after creating the instances
        if hasattr(document_class, "post_save"):
            signals.post_save.connect(document_class.post_save, sender=document_class)

        return instances if _quantity > 1 else instances[0]

    def _generate_mock_data(self, field):
        """Generate mock data based on field type."""
        if isinstance(field, fields.StringField):
            return faker.word()
        elif isinstance(field, fields.IntField):
            return faker.random_int(min=0, max=100)
        elif isinstance(field, fields.FloatField):
            return faker.pyfloat(min_value=0.1, max_value=1000)
        elif isinstance(field, fields.BooleanField):
            return faker.boolean()
        elif isinstance(field, fields.DateTimeField):
            return faker.date_time_this_decade()
        elif isinstance(field, fields.ListField):
            return [faker.word() for _ in range(2)]
        elif isinstance(field, fields.DictField):
            return {"key": faker.word(), "value": faker.word()}
        elif isinstance(field, fields.ObjectIdField):
            return ObjectId()
        elif isinstance(field, fields.EmbeddedDocumentField):
            return self.make(field.document_type)
        elif isinstance(field, fields.ReferenceField):
            return self.make(field.document_type)
        return None

    def cleanup(self):
        """Delete all created instances."""
        for instance in self._created_instances:
            instance.delete()
        self._created_instances.clear()


baker = Baker()
