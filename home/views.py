# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings
from models import *

def home(request):
    template_name = 'home/home.html'

    email = None
    if request.user.is_authenticated():
        email = request.user.username
    user = Personne.objects.get(email = email)

    def get_name():
        return user.nom
    def get_firstname():
        return user.prenom
    def get_email():
        return user.email
    def get_telephone():
        return user.telephone
    def get_poste():
        return user.poste

    return render(request, template_name, {'nom': get_name(), 'prenom' : get_firstname(),
     'email' : get_email(), 'telephone' : get_telephone(), 'poste' : get_poste()})


def logFail(request):
    return HttpResponse("Erreur d'authentification. \n Identifiant ou mot de passe incorrect")

class LoginView(TemplateView):

  template_name = 'front/index.html'

  def post(self, request, **kwargs):

    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )

    return HttpResponseRedirect('loginFail/')

class LogoutView(TemplateView):

  template_name = 'front/index.html'

  def get(self, request, **kwargs):

    logout(request)

    return render(request, self.template_name)
