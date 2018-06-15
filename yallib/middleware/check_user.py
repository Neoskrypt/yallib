from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import requires_csrf_token
from django.template import TemplateDoesNotExist, loader
from django.utils.deprecation import MiddlewareMixin


class CheckUser(MiddlewareMixin):
    # check user status
    def pre_request(self, request):
        if request.user.is_authenticated() and request.user.status != "LOCKED":
            return None
        elif not request.user.is_authenticated():  # anonymous user
            return None
        else:
            raise HttpResponseForbidden("<h1>403 Forbidden</h1>")
            ###################################################################
            # forbidden
	return True
