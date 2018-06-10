from django.db import models
from datetime import datetime


class BookManager(models.Manager):
    def get_by_natural_key(self, a, b, c):
        return self.get(first_name=a, last_name=b, date_birth=c)

class BaseModel(models.Model):
    created = models.DateTimeField(default=datetime.now, blank=True)
    changed = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Author(BaseModel):
    objects = BookManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField()

    class Meta:
        unique_together = (("first_name", "last_name", "date_birth"))

class Publication(BaseModel):
    caption = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name="authors")
    class Meta:
        abstract = True

class Genre(BaseModel):
    name = models.CharField(max_length=100)

class Book(Publication):
    genres = models.ManyToManyField(Author, related_name="genres")
