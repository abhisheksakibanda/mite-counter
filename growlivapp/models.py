from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Business(User):
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(blank=True, null=True, max_length=50)
    business_name = models.CharField(max_length=50)
    business_phone = PhoneNumberField()
    contact_person_name = models.CharField(max_length=50)
    contact_person_mobile = PhoneNumberField()

    class Meta:
        verbose_name_plural = "Businesses"


class Video(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, default=None)
    video = models.FileField(upload_to='mite_videos', validators=[FileExtensionValidator(
        allowed_extensions=['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm'])])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.video.name
