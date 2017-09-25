# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from models import *
from home.models import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class ImpressionView(TemplateView):
    template_name = 'impression.html'

    def post(self, request):
        if 'addToDatabase' in request.POST:

            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)
            prenomFournisseur = request.POST.get("prenomFournisseur", False)
            nomFournisseur = request.POST.get("nomFournisseur", False)
            date = request.POST.get("date", False)
            nombrePagesCouleur = request.POST.get("nombrePagesCouleur", False)
            nombrePagesNB = request.POST.get("nombrePagesNB", False)
            reliure = request.POST.get("reliure", False)
            estPaye = request.POST.get("estPaye", False)

            if not Personne.objects.filter(prenom = prenomFournisseur,
            nom = nomFournisseur) :
                return HttpResponse("Erreur : Fournisseur non membre TNS")

            prix = 0.1*float(nombrePagesCouleur) + 0.05*float(nombrePagesNB)
            if reliure:
                if Personne.objects.filter(prenom = prenomClient,
                nom = nomClient) :
                    prix += 0.5
                else :
                    prix +=1

            if reliure == 'oui':
                reliure = True
            else :
                reliure = False

            if estPaye == 'oui':
                estPaye = True
            else:
                estPaye = False

            Impression(date = date,
            nomClient = nomClient,
            prenomClient = prenomClient,
            nomFournisseur = nomFournisseur,
            prenomFournisseur = prenomFournisseur,
            nombrePagesCouleur = nombrePagesCouleur,
            nombrePagesNB = nombrePagesNB,
            reliure = reliure,
            prix = prix,
            estPaye = estPaye).save()


            msg = MIMEMultipart()
            msg['From'] = 'impression@tnservices.fr'
            msg['To'] = prenomClient + '.' + nomClient + '@telecomnancy.net'
            msg['Subject'] = 'Impression TNS'
            message = '''L'impression que vous avez demandée a été réalisée et est disponible au local.\n
            Il vous sera demandé la somme de : ''' + str(prix) + '''€.\n Sans cela votre impression ne vous sera pas remise.'''
            message = message.encode("utf-8")
            msg.attach(MIMEText(message))
            mailserver = smtplib.SMTP('smtp.gmail.com', 587)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.ehlo()
            mailserver.login('impression@tnservices.fr', 'impressionERP')
            mailserver.sendmail('impression@tnservices.fr', prenomClient + '.' + nomClient + '@telecomnancy.net', msg.as_string())
            mailserver.quit()


            return HttpResponse("Impression ajoutée")

        elif 'listTransactions' in request.POST:

            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)

            transactions = Impression.objects.filter(prenomClient = prenomClient, nomClient = nomClient, estPaye = False)

            return render(request, "transactions.html", {'nom': nomClient, 'prenom' : prenomClient,
              'transactions' : transactions})

        elif 'debts' in request.POST:
            id = request.POST.get("id")

            impression = Impression.objects.get(id = id)

            impression.estPaye = True
            impression.save()
            return HttpResponse("Impression validée")
