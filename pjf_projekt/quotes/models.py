from django.conf import settings
from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    fullname = models.CharField(max_length=120, null=False)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)


class Quote(models.Model):
    quote = models.CharField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, default=None, null=True)
