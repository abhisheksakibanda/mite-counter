# GrowLivApp/admin.py
from django.contrib import admin
from .models import Business, CustomUser, Photo

admin.site.register(Business)
admin.site.register(CustomUser)
admin.site.register(Photo)