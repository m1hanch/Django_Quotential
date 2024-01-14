import json


from mongoengine import StringField, DateField, Document, ListField, ReferenceField, connect
import os
from dotenv import load_dotenv
# Load secret .env file
load_dotenv()
connect(db='pjf_projekt',
        host=f'mongodb+srv://mihanch:{os.getenv("MONGO_PASS")}@cluster0.xo49jrs.mongodb.net/')


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


if __name__ == '__main__':
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    authors = []
    for item in authors_data:
        try:
            authors.append(Authors(**item))
        except Exception as e:
            print(f"Error processing author: {item}. Error: {e}")
    Authors.objects.insert(authors)

    author_mapping = {author.fullname: author for author in Authors.objects}

    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)

    quotes = []
    for item in quotes_data:
        author_name = item['author']
        author = author_mapping.get(author_name)
        if author:
            item['author'] = author
            quotes.append(Quotes(**item))

    Quotes.objects.insert(quotes)
