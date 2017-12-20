# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


# Permet d'administrer la table Impression depuis l'interface d'administration
admin.site.register(Impression)
