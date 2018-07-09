"""
yallib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import yallib.views as views
import yallib.class_views as class_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Use static()to add url mapping to serve static files during development(only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += i18n_patterns(

    path(_('login/authors/'), views.get_authors, name='authors'),
    path(_('login/author/<int:id>'), views.get_author, name="author"),
    path(_('login/'), views.login, name='login'),
    path(_('login/authorview/<int:id>'), class_views.AuthorView.as_view()),
    path(_('login/authorlist/'), class_views.AuthorListView.as_view(), name="authorlist"),
    path(_('author/<int:id>/update/'), class_views.AuthorUpdate.as_view()),
    path(_('author/<int:id>/delete/'), class_views.AuthorDelete.as_view()),
    # path('logout/', views.logout),
)

SERVER_ENVIRONMENT = os.getenv('RUN_ENV', '')
if SERVER_ENVIRONMENT == 'PROD':
    urlpatterns += path('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
