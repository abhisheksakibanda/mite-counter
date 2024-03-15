from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    contact_person_name = models.CharField(max_length=255)
    contact_person_mobile = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "Businesses"


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    image = models.ImageField(upload_to='mite_img')
    description = models.TextField(blank=True, null=True)
