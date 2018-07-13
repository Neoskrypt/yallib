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
import yallib.views1 as views1
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('admin/', admin.site.urls),

]
urlpatterns += i18n_patterns(
    path(_('authors/'), views.get_authors, name='authors'),
    path(_('author/<int:id>'), views.get_author, name="author"),
    path(_('login/'), views.login, name='login'),
    path(_('authorview/<int:id>'), views1.AuthorView.as_view()),
    path(_('authorlist/'), views1.AuthorListView.as_view(), name="authorlist"),
    # path('logout/', views.logout),
) + [
    path('', views.get_authors, name="home"),
]