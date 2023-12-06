from django.forms import ModelForm, CharField, TextInput, CheckboxSelectMultiple, Select

from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=120, widget=TextInput(attrs={"class": "form-control",
                                                                 "id": "exampleInputAuthor"}))
    born_date = CharField(max_length=50,
                          widget=TextInput(attrs={"class": "form-control", "id": "exampleInputBornDate"}))
    born_location = CharField(max_length=120,
                              widget=TextInput(attrs={"class": "form-control", "id": "exampleInputBornLocation"}))
    description = CharField(
        widget=TextInput(attrs={"class": "form-control", "id": "exampleInputDescription"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(max_length=100)

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = TextInput()
    tags = CharField(widget=TextInput(), required=False)
    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = Select()
