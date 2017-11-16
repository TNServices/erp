# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from home.models import *

# Permet d'administrer la table Personne depuis l'interface d'administration

admin.site.register(Personne)
