from mongoengine import connect, Document, StringField, DateField, ListField, ReferenceField
import os
from dotenv import load_dotenv
load_dotenv()

conn = connect(db='hw10', host=f'mongodb+srv://mihanch:{os.getenv("MONGO_PASS")}@cluster0.xo49jrs.mongodb.net/')


class Authors(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = StringField()
    born_location = StringField(max_length=120)
    description = StringField(max_length=5000)
    meta = {'collection': 'authors'}


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField('Authors')
    quote = StringField(max_length=200)
    meta = {'collection': 'quotes'}
