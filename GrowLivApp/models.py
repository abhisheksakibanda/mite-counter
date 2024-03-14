# GrowLivApp/models.py
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    contact_person_name = models.CharField(max_length=255)
    contact_person_mobile = models.CharField(max_length=15)
    # Add other fields as needed

class CustomUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # Add other fields as needed
class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    image = models.ImageField(upload_to='mite_photos/')
    description = models.TextField(blank=True, null=True)
