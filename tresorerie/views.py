# -*- coding: utf-8 -*-

# Gère l'interface trésorerie, notamment la page d'accueil, la page qui liste les recettes par mois
# et la page qui liste les impayés

from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from impression.models import *
from home.models import *
from django.db.models import *

# Affiche la page d'accueil trésorerie
class TresorerieView(TemplateView):

    # On vérifie que l'utilisateur courant est 'Trésorier' ou 'Vice Trésorier'
    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'tresorerie.html'
            return render(request, template_name)
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")


# Page qui liste les impayés à ce jour
class ImpayesView(TemplateView):
    def get(self, request):

        # On vérifie le poste
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':

        # On affiche le template 'impayes.html'
            template_name = 'impayes.html'

        # On retourne le template avec la liste des transactions qui ont l'attribut estPaye = False
            impayes = Impression.objects.filter(estPaye = False)
            return render(request, template_name, {'impayes' : impayes})
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")



# Affiche la liste des recettes par mois
class RecettesView(TemplateView):
    def get(self, request):
        # On vérifie le poste
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'recettes.html'

            # On a la liste des dates de la table Impression
            dates = Impression.objects.values('date')
            tab = []
            # On tronc les dates au mois
            for date in dates :
                tab.append(str(date['date'])[:7])
            tab = set(tab)

            liste = {}

            # Pour chaque mois dans le set, on regarde toutes les transactions dont la date commence par ce mois là
            # et somme les prix des estPaye = True
            for mois in set(tab):
                recettes = Impression.objects.filter(estPaye = True, date__startswith = mois)
                somme_prix = 0
                for recette in recettes:
                    somme_prix += recette.prix
                liste[mois] = somme_prix

            # On retourne la liste et le template 'recettes.html'
            return render(request, template_name, {'recettes' : liste})
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")
