from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField

class Contacts(Document):
    fullname = StringField()
    email = StringField()
    status = BooleanField(default=False)

