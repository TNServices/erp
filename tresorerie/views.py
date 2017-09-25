# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from impression.models import *
from home.models import *
from django.db.models import *


class TresorerieView(TemplateView):

    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'tresorerie.html'
            return render(request, template_name)
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")

class ImpayesView(TemplateView):
    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'impayes.html'

            impayes = Impression.objects.filter(estPaye = False)
            return render(request, template_name, {'impayes' : impayes})
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")

class RecettesView(TemplateView):
    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'recettes.html'

            dates = Impression.objects.values('date')
            tab = []
            for date in dates :
                tab.append(str(date['date'])[:7])
            tab = set(tab)

            liste = {}
            for mois in set(tab):
                recettes = Impression.objects.filter(estPaye = True, date__startswith = mois)
                somme_prix = 0
                for recette in recettes:
                    somme_prix += recette.prix
                liste[mois] = somme_prix

            return render(request, template_name, {'recettes' : liste})
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")
