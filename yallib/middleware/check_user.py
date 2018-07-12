from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class CheckUser(MiddlewareMixin):
    # check user status
    def pre_request(self, request):

        if request.user.is_authenticated() and request.user.status != "LOCKED":
            return None

        elif request.user.is_anonymous():  # anonymous user
            return True
        else:
            raise HttpResponseForbidden("<h1>403 Forbidden</h1>")
            return True
