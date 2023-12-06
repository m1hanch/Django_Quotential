from mongoengine import connect, Document, StringField, DateField, ListField, ReferenceField


conn = connect(db='hw10', host='mongodb+srv://mihanch:mihaJ0107@cluster0.xo49jrs.mongodb.net/')


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
