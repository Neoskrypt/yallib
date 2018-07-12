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
import yallib.views.views as views
import yallib.views.class_views as class_views
from django.conf import settings
from django.views.generic.base import TemplateView
import os


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # path('login/authors/', views.get_authors, name='authors'),
    # path('login/author/<int:id>', views.get_author, name="author"),
    path('login/', views.login, name='login'),
    path('login/authorview/<int:id>', class_views.AuthorView.as_view()),
    path('login/author/list/', class_views.AuthorListView.as_view(), name="authorlist"),
    path('author/<int:id>/update/', class_views.AuthorUpdate.as_view()),
    path('author/<int:id>/delete/', class_views.AuthorDelete.as_view()),
    # path('logout/', views.logout),
]
# for static with help gunicorn
SERVER_ENVIRONMENT = os.getenv('RUN_ENV', '')
if SERVER_ENVIRONMENT == 'PROD':
    urlpatterns += path('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
