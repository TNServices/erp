# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings
from models import *

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get (self, request):
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

        return render(request, self.template_name, {'nom': get_name(), 'prenom' : get_firstname(),
          'email' : get_email(), 'telephone' : get_telephone(), 'poste' : get_poste()})



    def post(self, request, **kwargs):
        oldPassword = request.POST.get('oldPassword', False)
        newPassword1 = request.POST.get('newPassword1', False)
        newPassword2 = request.POST.get('newPassword2', False)

        user = authenticate(username=request.user.username, password=oldPassword)
        if user is not None and user.is_active:
            if newPassword1 == newPassword2:
                request.user.set_password(newPassword1)
                request.user.save()
                return HttpResponse("Mot de passe mis à jour")
            else :
                return HttpResponse("Erreur. Les deux mots de passe ne correspondent pas")
        else:
            return HttpResponse("Erreur. L'ancien mot de passe ne correspond pas au compte")


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
