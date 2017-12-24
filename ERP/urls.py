"""ERP URL Configuration

Fichier des tables de routage.
Index des urls du site web.


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from home.views import *
from impression.views import *
from tresorerie.views import *
from django.contrib.auth.decorators import login_required
from django.conf.urls import include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', LoginView.as_view()),
    url(r'^home/$', login_required(HomeView.as_view())),
    url(r'^index/$', login_required(IndexView.as_view())),
    url(r'^account/$', login_required(AccountView.as_view())),
    url(r'^loginFail/$', logFail),
	url(r'^accounts/', include('allauth.urls')),
    url(r'^impressions/$', login_required(ImpressionView.as_view())),

    url(r'^tresorerie/$', login_required(TresorerieView.as_view())),
    url(r'impayes/$', login_required(ImpayesView.as_view())),
    url(r'recettes/$', login_required(RecettesView.as_view()))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
