# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Gère la page d'accueil des immpressions et la liste des transactions non payées d'une personne

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from django import forms

from .models import *

from home.models import *
import os
import time

class ImpressionView(TemplateView):
    template_name = 'impression.html'

    def post(self, request):

        # Si le post vient du bouton 'addToDatabase'
        if 'addToDatabase' in request.POST:

            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)

            user = Personne.objects.get(email = request.user.username)
            prenomFournisseur = user.prenom
            nomFournisseur = user.nom
            date = time.strftime('%Y-%m-%d',time.localtime())

            nombrePagesCouleur = request.POST.get("nombrePagesCouleur", False)
            nombrePagesNB = request.POST.get("nombrePagesNB", False)
            reliure = request.POST.get("reliure")
            estPaye = request.POST.get("estPaye")
            email = request.POST.get("email")

            print(reliure)

            print(estPaye)


            # Si le fournisseur n'est pas dans la table Personne (donc pas membre TNS)
            if not Personne.objects.filter(prenom = prenomFournisseur,
            nom = nomFournisseur) :
                return HttpResponse("Erreur : Fournisseur non membre TNS")


            # Calcul du prix : réduction sur la reliure pour les membres TNS
            prix = 0.1*float(nombrePagesCouleur) + 0.05*float(nombrePagesNB)
            if reliure == 'oui':
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


            if email == 'oui':

                # On envoie un mail au client lui disant que sa commande est prête
                command = ''' echo "L'impression que vous avez demandée a été réalisée et est disponible au local.\n
                Il vous sera demandé la somme de ''' + str(prix) + '''€. \n
                Sans cette somme, votre impression ne vous sera pas remise.\n
                \t Cordialement, l'équipe de TNS" | mail -s "Impression TNS" ''' + prenomClient + '''.''' + nomClient + '''@telecomnancy.net'''

                os.system(command.encode('utf-8'))


            return HttpResponse("Impression ajoutée")

        #Si post vient du bouton 'listAllTransactions'
        elif 'listAllTransactions' in request.POST:

            #On regarde dans la table Impression toutes les impressions non payees
            transactions= Impression.objects.filter(estPaye = False)

            #On renvoie 'transactionsAll.html' avec les informations
            return render(request, "transactionsAll.html", {'transactions':transactions})


            #Si le post vient du bouton 'transactionsAll_debts'
        elif 'transactionsAll_debts' in request.POST:

            # On a l'identifiant de la transaction
            id = request.POST.get("id")

            # On regarde dans la table Impression la transaction avec cet identifiant
            impression = Impression.objects.get(id = id)

            # On modifie l'attribut 'estPaye'
            impression.estPaye = True
            impression.save()

            #On regarde dans la table Impression toutes les impressions non payees
            transactions= Impression.objects.filter(estPaye = False)

            #On renvoie 'transactionsAll.html' avec les informations
            return render(request, "transactionsAll.html", {'transactions':transactions})


        # Si le post vient du bouton 'listTransactions'
        elif 'listTransactions' in request.POST:

            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)

            # On regarde dans la table Impression toutes les transactions de ce client
            transactions = Impression.objects.filter(prenomClient = prenomClient, nomClient = nomClient, estPaye = False)

            # On renvoie 'transactions.html' avec les informations sur les transactions du client
            return render(request, "transactions.html", {'nom': nomClient, 'prenom' : prenomClient,
              'transactions' : transactions})


        # Si le post vient du bouton 'debts' du template 'transactions.html'
        elif 'debts' in request.POST:

            # On a l'identifiant de la transaction
            id = request.POST.get("id")

            # On regarde dans la table Impression la transaction avec cet identifiant
            impression = Impression.objects.get(id = id)

            # On modifie l'attribut 'estPaye'
            impression.estPaye = True
            impression.save()
            return HttpResponse("Impression validée")
