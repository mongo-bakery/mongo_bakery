import importlib
import inspect
import re
import sys
from contextlib import ExitStack
from typing import Any
from unittest.mock import MagicMock, patch

from faker import Faker
from mongoengine import Document, EmbeddedDocument, signals

from mongo_bakery.sequences import Sequence

faker = Faker()
bakery_fields_generators = importlib.import_module("mongo_bakery.bakery_fields_generators")


class Baker:
    def __init__(self, mock_class=None):
        self._dependencies_to_patch = mock_class or []
        self._created_instances = []
        self._generation_chain = []

    def mock_dependencies(self, mock_class: list):
        """
        Mocks the specified dependencies for testing purposes.

        Args:
            mock_class (list): A list of classes or modules to be mocked.
        """
        self._dependencies_to_patch = mock_class

    def make(
        self, document_class: type[Document], _quantity: int = 1, **kwargs: dict[Any, Any]
    ) -> Document | list[Document]:
        """
        Creates and saves one or more instances of a MongoEngine document.

        Args:
            document_class (type[Document]): The MongoEngine document class to instantiate.
            _quantity (int, optional): The number of instances to create. Defaults to 1.
            **kwargs: Additional field values to set on the document instances.

        Returns:
            Document or list[Document]: A single document instance if _quantity is 1,
            otherwise a list of document instances.

        Raises:
            ValueError: If the provided document_class is not a subclass of mongoengine.Document
                or mongoengine.EmbeddedDocument.
        """
        if not (issubclass(document_class, Document) or issubclass(document_class, EmbeddedDocument)):
            raise ValueError("The document must be a subclass of mongoengine.Document or mongoengine.EmbeddedDocument")

        if document_class in self._generation_chain:
            chain_repr = " -> ".join(cls.__name__ for cls in [*self._generation_chain, document_class])
            raise ValueError(
                f"Cycle detected while generating mock data for required fields: {chain_repr}. "
                "Pass an explicit value via kwargs to break the cycle."
            )

        self._generation_chain.append(document_class)
        try:
            patch_dependencies = {}
            module_name = document_class.__module__

            if self._dependencies_to_patch and module_name in sys.modules:
                module = sys.modules[module_name]
                try:
                    source_lines = inspect.getsource(module).splitlines()
                except (OSError, TypeError):
                    source_lines = []
                for dep in self._dependencies_to_patch:
                    if any(re.search(rf"\b{re.escape(dep)}\b", line) for line in source_lines):
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
                    for field_name, value in instance_data.items():
                        if isinstance(value, Sequence):
                            instance_data[field_name] = value()

                    instance = document_class(**instance_data)
                    if not issubclass(document_class, EmbeddedDocument):
                        instance.save()
                        self._created_instances.append(instance)
                    instances.append(instance)

            # Reconnect the signal after creating the instances
            if hasattr(document_class, "post_save"):
                signals.post_save.connect(document_class.post_save, sender=document_class)

            return instances if _quantity > 1 else instances[0]
        finally:
            self._generation_chain.pop()

    def seq(self, value, increment_by=1, start=None):
        """
        Build a sequence that yields an incrementing value each time `make` creates an instance.

        Args:
            value: The base value. Supported types are str, int, float, date and datetime.
            increment_by: The amount added on every call. Defaults to 1. For date/datetime values,
                this must be a timedelta.
            start: The offset applied on the first call. Defaults to `increment_by`.

        Returns:
            Sequence: A callable object that `make` resolves to a new value for each instance.
        """
        return Sequence(value, increment_by=increment_by, start=start)

    def seed(self, value):
        """
        Seed Faker's shared random generator, so `make` produces reproducible mock data.

        `Faker.seed` seeds a random generator shared by every `Faker()` instance by default,
        so this affects mock data generated anywhere in mongo_bakery, not just this module.

        Args:
            value: The seed value, passed through to `Faker.seed`.
        """
        Faker.seed(value)

    def _generate_mock_data(self, field):
        """
        Generate mock data based on the provided field type.

        Args:
            field: The Field type used in the convention. @see the bakery_fields_generators module.

        Returns:
            Any: Mock data appropriate for the given field type.

        """
        if field.choices:
            return self._mock_choice(field)

        field_type = type(field).__name__
        mock_method_name = f"mock_{field_type}"
        mock_method = getattr(bakery_fields_generators, mock_method_name, self._mock_default)

        if field_type in {
            "EmbeddedDocumentField",
            "ReferenceField",
            "ListField",
            "EmbeddedDocumentListField",
            "MapField",
            "LazyReferenceField",
            "GenericReferenceField",
        }:
            return mock_method(field, self)
        return mock_method(field)

    def _mock_choice(self, field):
        """
        Pick a random value from a field's `choices` so the result always passes mongoengine's choices validation.

        Args:
            field: The Field instance whose `choices` attribute should be used.

        Returns:
            Any: One of the valid values declared in `field.choices`.
        """
        choice = faker.random_element(field.choices)
        return choice[0] if isinstance(choice, list | tuple) else choice

    def _mock_default(self, field):
        """When there is no match for the field type."""
        raise ValueError(f"No mock defined for field type: {type(field).__name__}")

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
