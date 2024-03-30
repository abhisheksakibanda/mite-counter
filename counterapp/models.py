from django.db import models

from growlivapp.models import Video


class Result(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    feeder_mite_count = models.IntegerField(default=0)
    predator_mite_count = models.IntegerField(default=0)
    scan_date = models.DateTimeField(auto_now_add=True)
