from django.contrib.admin import ModelAdmin
from django.contrib.admin import register


import yallib.models as models


@register(models.Author)
class AuthorAdmin(ModelAdmin):
        pass
@register(models.User)
class UserAdmin(ModelAdmin):
    pass
