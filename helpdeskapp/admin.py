from django.contrib import admin
from .models import *

admin.site.register(Utilisateur),
admin.site.register(Demande),
admin.site.register(Domaine),

# Register your models here.
