from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class CheckUser(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    # check user status
    def __call__(self, request):
        # import pdb; pdb.set_trace()
        if request.user.is_authenticated and request.user.status != "LOCKED" or request.user.is_anonymous:
            return self.get_response(request)

        else:
            raise HttpResponseForbidden("<h1>403 Forbidden</h1>")
