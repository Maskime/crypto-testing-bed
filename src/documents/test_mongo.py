from datetime import datetime

from mongoengine import Document, StringField, DateTimeField


class TestMongo(Document):
    title: StringField(max_length=200, required=True)
    date_modified: DateTimeField(default=datetime.utcnow)
