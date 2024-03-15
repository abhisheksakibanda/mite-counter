from django.db import models

from growlivapp.models import Photo


class Result(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    feeder_mite_count = models.IntegerField(default=0)
    predator_mite_count = models.IntegerField(default=0)
    obj_detection_image = models.ImageField(upload_to='pred_mites')
    scan_date = models.DateTimeField(auto_now_add=True)
