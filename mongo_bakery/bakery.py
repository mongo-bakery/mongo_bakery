from mongoengine import Document


class Baker:
    def make(self, document_class: Document) -> Document:
        return document_class()


baker = Baker()
