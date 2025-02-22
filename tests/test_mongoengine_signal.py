from unittest.mock import patch

from mongoengine import Document, IntField, StringField, signals

from mongo_bakery import baker


def test_signals_disconnected_and_reconnected():
    """
    Test that signals are properly disconnected and reconnected when creating a document.

    This test defines a `DocumentWithSignals` class with `name` and `age` fields and a `post_save` signal handler.
    It connects the `post_save` signal to the `post_save` handler of `DocumentWithSignals`.

    Assertions:
    - `mock_connect.assert_called_once_with(DocumentWithSignals.post_save, sender=DocumentWithSignals)`
    """

    class DocumentWithSignals(Document):
        name = StringField(required=True)
        age = IntField(required=True)

        meta = {"collection": "test_documents"}

        @classmethod
        def post_save(cls, sender, document, **kwargs):
            raise Exception("this code don't run")  # pragma: no cover

    signals.post_save.connect(DocumentWithSignals.post_save, sender=DocumentWithSignals)

    with (
        patch.object(signals.post_save, "connect") as mock_connect,
    ):
        baker.make(DocumentWithSignals)
        mock_connect.assert_called_once_with(DocumentWithSignals.post_save, sender=DocumentWithSignals)
