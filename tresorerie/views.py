# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from impression.models import *
from home.models import *

class TresorerieView(TemplateView):

    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'tresorerie.html'
            return render(request, template_name)
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")

    def post(self, request):
        if 'recettes' in request.POST:
            mois = request.POST.get("mois")
            recettes = Impression.objects.filter(date__startswith = mois)
            prix = 0
            for transaction in recettes:
                prix += transaction.prix

            return render(request, "recettes.html", {'mois': mois, 'prix' : prix})

class ImpayesView(TemplateView):
    def get(self, request):
        email = request.user.username
        user = Personne.objects.get(email = email)
        if user.poste == 'Trésorier' or user.poste == 'Vice Trésorier':
            template_name = 'impayes.html'

            impayes = Impression.objects.filter(estPaye = False)
            print impayes
            return render(request, template_name, {'impayes' : impayes})
        else :
            return HttpResponse("T'as cru t'étais trésorier ou quoi ?")
