from django.db import models

from utils.models import AliveManager, TimeStampedModel


class Word(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    alive_objects = AliveManager()
