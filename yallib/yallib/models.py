from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    changed = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        abstract = True


class Author(BaseModel):
    name = models.CharField(max_length=100)
    date_birth = models.DateField()


class Publication(BaseModel):
    caption = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author,related_name="authors")

    class Meta:
        abstract = True


class Genre(BaseModel):
    name = models.CharField(max_length=100)


class Book(Publication):
    genres = models.ManyToManyField(Author,related_name="genres")
