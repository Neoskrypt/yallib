from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import requires_csrf_token
from django.template import TemplateDoesNotExist, loader
ERROR_403_TEMPLATE_NAME = '403.html'

"""
@requires_csrf_token
def permission_denied(request, exception, template_name=ERROR_403_TEMPLATE_NAME):

    Permission denied (403) handler.

    Templates: :template:`403.html`
    Context: None

    If the template does not exist, an Http403 response containing the text
    "403 Forbidden" (as per RFC 7231) will be returned.

    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_403_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseForbidden(
            "<h1>403 Forbidden</h1>", content_type='text/html'
            )
    return HttpResponseForbidden(
        template.render(request=request, context={"\
        exception": str(exception)})
    )
    """

class CheckUser(object):
    # check user status
    def pre_request(self, request):
        if request.user.is_authenticated() and request.user.status != "LOCKED":
            return None
        elif not request.user.is_authenticated():  # anonymous user
            return None
        else:
            # forbidden
            @requires_csrf_token
            def permission_denied(request, exception, template_name=ERROR_403_TEMPLATE_NAME):
                
                """
                Permission denied (403) handler.

                Templates: :template:`403.html`
                Context: None

                If the template does not exist, an Http403 response containing the text
                "403 Forbidden" (as per RFC 7231) will be returned.
                """
                try:
                    template = loader.get_template(template_name)
                except TemplateDoesNotExist:
                    if template_name != ERROR_403_TEMPLATE_NAME:
                        # Reraise if it's a missing custom template.
                        raise
                    return HttpResponseForbidden(
                        "<h1>403 Forbidden</h1>", content_type='text/html'
                        )
                return HttpResponseForbidden(
                    template.render(request=request, context={"\
                    exception": str(exception)})
                )
