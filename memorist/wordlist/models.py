from django.db import models

from utils.models import AliveManager


class Word(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()
    alive_objects = AliveManager()
