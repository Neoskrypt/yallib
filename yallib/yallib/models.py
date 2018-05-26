from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField()
    changed = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
class Author(BaseModel):
    name = models.CharField(max_lenght=100)
    date_birth = models.DateField()
class Publication(BaseModel):
    caption = CharField(max_lenght=50)
    authors = models.ManyToManyField(Author)
    class Meta:
        abstract = True
class Genre(BaseModel):
    name = models.CharField(max_lenght=100)
class Book(Publication):
    genres = models.ManyToManyField(Author)
