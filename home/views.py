# -*- coding: utf-8 -*-

# Vue principale de l'application home
# Elle gère la page de login, la page d'index, la page d'accueil et la page de modification des informations du compte

from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings

from .models import *


# Affiche la page d'index

class IndexView(TemplateView):
    template_name = 'front/index.html'

    def get (self, request):
        dansLaBaseDeDonee = True;

        try :
            user = Personne.objects.get(email = request.user.username)
        except :
            dansLaBaseDeDonee = False;

        return render(request, self.template_name, {'dansLaBaseDeDonee' : dansLaBaseDeDonee})




# Affiche la page de modification des informations du compte

class AccountView(TemplateView):
    template_name = 'front/account.html'

    def post(self, request):

        # Si le post viens du bouton 'password'

        if 'password' in request.POST:

            oldPassword = request.POST.get('oldPassword', False)
            newPassword1 = request.POST.get('newPassword1', False)
            newPassword2 = request.POST.get('newPassword2', False)

            # On vérifie que l'ancien mot de passe est le bon
            user = authenticate(username=request.user.username, password=oldPassword)
            if user is not None and user.is_active:
                if newPassword1 == newPassword2:
                    # On modifie la base de données utilisateurs
                    request.user.set_password(newPassword1)
                    # On sauvegarde les modifications
                    request.user.save()
                    return HttpResponse("Mot de passe mis à jour")
                else :
                    return HttpResponse("Erreur. Les deux mots de passe ne correspondent pas")
            else:
                return HttpResponse("Erreur. L'ancien mot de passe ne correspond pas au compte")


        # si le post vient du bouton 'téléphone'
        elif 'telephone' in request.POST :

            telephone = request.POST.get('Téléphone', False)

            if request.user.is_authenticated():
                email = request.user.username

            # On cherche dans la table Personne l'utilisateur courant
            user = Personne.objects.get(email = email)
            user.telephone = telephone
            # On modifie et sauvegarde son numéro de téléphone dans la table Personne
            user.save()

            return HttpResponse("Numéro de Téléphone modifié")
	    # On cherche dans la base les informations relatives à l'utilisateur courant
    def get (self, request):
        email = None

        if request.user.is_authenticated():
            email = request.user.username

        #print(email);

        #user = Personne.objects.get(email=email)
        user = get_object_or_404(Personne, email=email)

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

        # On retourne le template html avec les informations sur l'utilisateur
        return render(request, self.template_name, {'nom': get_name(), 'prenom' : get_firstname(),
          'email' : get_email(), 'telephone' : get_telephone(), 'poste' : get_poste()})


# Affiche la page d'accueil
class HomeView(TemplateView):
    template_name = 'home/home.html'
    	    # On cherche dans la base les informations relatives à l'utilisateur courant
    def get (self, request):
        email = None

        if request.user.is_authenticated:
            email = request.user.username

        #print(email);

        #user = Personne.objects.get(email=email)
        user = get_object_or_404(Personne, email=email)

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

        # On retourne le template html avec les informations sur l'utilisateur
        return render(request, self.template_name, {'nom': get_name(), 'prenom' : get_firstname(),
          'email' : get_email(), 'telephone' : get_telephone(), 'poste' : get_poste()})





    # retourne une erreur
def logFail(request):
    return HttpResponse("Erreur d'authentification. \n Identifiant ou mot de passe incorrect")


# Affiche la page de login
class LoginView(TemplateView):

  template_name = 'front/login.html'

  def post(self, request, **kwargs):

    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    # On vérifie si les identifiants permeettent de se connecter
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect( '/index/' )

    return HttpResponseRedirect('loginFail/')
