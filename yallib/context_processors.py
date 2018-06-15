from django.conf import settings

#########################################################


def menu(request):

    return {
        "site_name": settings.SITE_NAME,
        "site_description": settings.SITE_DESCRIPTION
        }
