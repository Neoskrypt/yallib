from django.conf import settings
from django.core.context_processors import request
#########################################################


def menu(request):

    return {
        "site_name": settings.SITE_NAME,
        "site_description": settings.SITE_DESCRIPTION
        }
