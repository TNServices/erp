# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Gère la page d'accueil des immpressions et la liste des transactions non payées d'une personne

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import *
from django import forms

import operator
import csv

from .models import *

from home.models import *
import os
import time

class ImpressionView(TemplateView):
    template_name = 'impression.html'

    def post(self, request):

        #Retourne la liste des dix dernieres impressions
        def getDixDernieresTransactions():
            # On regarde dans la table Impression les dix dernieres impressions
            transactions = Impression.objects.all()
            if len(transactions) > 10:
                transactions = transactions[len(transactions)-10:]

            transactions_ordonnees = sorted(
                transactions, key=operator.attrgetter('date'))
            transactions_ordonnees.reverse()
            return transactions_ordonnees

        #Retourne la liste des impressions non payees
        def getUnpaidTransactions():
            #On regarde dans la table Impression toutes les impressions non payees
            transactions= Impression.objects.filter(estPaye = False)
            transactions_ordonnees = sorted(transactions, key=operator.attrgetter('date'))
            transactions_ordonnees.reverse()
            #On renvoie 'transactionsAll.html' avec les informations
            return transactions_ordonnees


        # Si le post vient du bouton 'addToDatabase'
        if 'addToDatabase' in request.POST:

            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)

            user = Personne.objects.get(email = request.user.username)
            prenomFournisseur = user.prenom
            nomFournisseur = user.nom
            date = time.strftime('%Y-%m-%d',time.localtime())

            nombrePagesCouleur = request.POST.get("nombrePagesCouleur", False)
            nombrePagesNB = float(request.POST.get("nombrePagesTotal", False)) - float(nombrePagesCouleur)
            if (nombrePagesNB < 0):
                return HttpResponse("Erreur : Nombre de pages total < Nombre de pages en couleur")
            reliure = request.POST.get("reliure")
            estPaye = request.POST.get("estPaye")
            email = 'non'
            nombre = request.POST.get("nombre")


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

            try :
                for i in range(int(nombre)):
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
            except:
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

            return render(request, "impressionAddedSuccess.html")

        #Si post vient du bouton 'listAllTransactionsUnpaid'
        elif 'listAllTransactionsUnpaid' in request.POST:
            transactions_ordonnees = getUnpaidTransactions()
            return render(request, "transactionsAllUnpaid.html", {'transactions':transactions_ordonnees})

        #Si post vient du bouton 'listAllTransactions'
        elif 'listAllTransactions' in request.POST:
            #On regarde dans la table Impression toutes les impressions non payees
            transactions= Impression.objects.filter()
            transactions_ordonnees = sorted(transactions, key=operator.attrgetter('date'))
            transactions_ordonnees.reverse()
            #On renvoie 'transactionsAll.html' avec les informations
            return render(request, "transactionsAll.html", {'transactions':transactions_ordonnees})


        #Si le post vient du bouton 'transactionsAllUnpaid_debts'
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
            transactions_ordonnees = sorted(transactions, key=operator.attrgetter('date'))
            transactions_ordonnees.reverse()
            #On renvoie 'transactionsAll.html' avec les informations
            return render(request, "transactionsAllUnpaid.html", {'transactions':transactions_ordonnees})


        # Si le post vient du bouton 'listTransactions'
        elif 'listTransactions' in request.POST:
            prenomClient = request.POST.get("prenomClient", False)
            nomClient = request.POST.get("nomClient", False)
            # On regarde dans la table Impression toutes les transactions de ce client
            transactions = Impression.objects.filter(prenomClient = prenomClient, nomClient = nomClient, estPaye = False)
            transactions_ordonnees = sorted(transactions, key=operator.attrgetter('date'))
            transactions_ordonnees.reverse()
            # On renvoie 'transactions.html' avec les informations sur les transactions du client
            return render(request, "transactions.html", {'nom': nomClient, 'prenom' : prenomClient,
              'transactions' : transactions_ordonnees})

	    # Si le post vient du bouton 'listTenLastTransactions'
        elif 'listTenLastTransactions' in request.POST:
            transactions_ordonnees = getDixDernieresTransactions()
            #On renvoie 'transactionsTen.html' avec les informations
            return render(request, "transactionsTenLast.html", {'transactions':transactions_ordonnees})

        # Si le post vient du bouton 'debts' du template 'transactions.html'
        elif 'debts' in request.POST:
            # On a l'identifiant de la transaction
            id = request.POST.get("id")
            # On regarde dans la table Impression la transaction avec cet identifiant
            impression = Impression.objects.get(id = id)
            # On modifie l'attribut 'estPaye'
            impression.estPaye = True
            impression.save()
            # On renvoie 'transactions.html' avec les informations sur les transactions du client
            return render(request, "impression.html")

        #Si le post vient du bouton delete du template 'transactionsTenLast.html'
        elif 'deleteFromTen' in request.POST:
            #On recupere l'identifiant
            id = request.POST.get("id")
            #On supprime
            impression = Impression.objects.get(id = id)
            impression.delete()
            #On renvoie 'transactionsTen.html' avec les informations
            transactions_ordonnees = getDixDernieresTransactions()
            return render(request, "transactionsTenLast.html", {'transactions':transactions_ordonnees})


        elif 'deleteFromAllUnpaid' in request.POST:
            #On recupere l'identifiant
            id = request.POST.get("id")
            #On supprime
            impression = Impression.objects.get(id = id)
            impression.delete()
            #On renvoie 'transactionsAllUnpaid.html'
            transactions_ordonnees = getUnpaidTransactions()
            return render(request, "transactionsAllUnpaid.html", {'transactions':transactions_ordonnees})

        elif 'listePersonnes' in request.POST:
            #On recupere la liste des personnes
            listePersonnes = Personne.objects.filter()
            listePersonnes = sorted(listePersonnes, key=operator.attrgetter('nom'))
            return render(request, "listepersonnes.html", {'personnes':listePersonnes})

        elif 'csvPourLaCompta' in request.POST:
            #Creer la réponse http
            date=request.POST.get("moisCSV")
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachement; filename="{0}.csv"'.format(date)
            #Writer
            writer = csv.writer(response)
            impressions = Impression.objects.filter()
            impressions = sorted(impressions, key=operator.attrgetter('date'))
            total = 0;
            writer.writerow(['Date','Nom','Prénom','Prix (euros)'])
            for impression in impressions:
                if str(impression.date).find(date)==0:
                    writer.writerow([impression.date, impression.nomClient, impression.prenomClient, impression.prix])
                    total+=impression.prix;
            writer.writerow(['','','Total (euros)',total])
            return response
