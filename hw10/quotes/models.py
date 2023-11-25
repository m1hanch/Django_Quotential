from django.db import models

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=120)
    born_date = models.DateTimeField()
    born_location = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)

class Quote(models.Model):
    tags = models.ManyToManyField('Author')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=200)

    class Meta:
        db_table = 'quotes'



