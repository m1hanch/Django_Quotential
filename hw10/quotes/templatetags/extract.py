from bson import ObjectId
from django import template
from ..utils import Authors

register = template.Library()


def get_author(id_):
    print(f"Type of id_ is: {type(id_)}")  # This should be <class 'str'> or <class 'bytes'>

    # Make sure that id_ is a string or bytes, not an Authors instance
    if not isinstance(id_, (str, bytes)):
        raise ValueError(f"Expected id_ to be a str or bytes, got {type(id_)} instead.")
    author = Authors.objects(id=ObjectId(id_)).first()
    return author.fullname


register.filter('author', get_author)


@register.filter(name='get_last_three_pages')
def get_last_three_pages(num_pages):
    return range(max(1, num_pages - 2), num_pages + 1)