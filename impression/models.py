# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Table Impression qui modélise une impression ou une reliure
class Impression(models.Model):
    date = models.DateField()
    nomClient = models.CharField(max_length = 100)
    prenomClient = models.CharField(max_length = 100)
    nomFournisseur = models.CharField(max_length = 100)
    prenomFournisseur = models.CharField(max_length = 100)
    nombrePagesCouleur = models.IntegerField()
    nombrePagesNB = models.IntegerField()
    reliure = models.BooleanField()
    prix = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix à régler")
    estPaye = models.BooleanField()

    def __unicode__(self):
        return "Id : {10} \n Date : {0} \n Client : {2} {1} \n Fournisseur : {4} {3} \n\
        {5} pages couleur \n {6} pages noir et blanc \n Reliure : {7} \n\
        Prix : {8} \n est payé : {9}".format(self.date, self.nomClient, self.prenomClient,
        self.nomFournisseur, self.prenomFournisseur, self.nombrePagesCouleur,
        self.nombrePagesNB, self.reliure, self.prix, self.estPaye, self.id)
