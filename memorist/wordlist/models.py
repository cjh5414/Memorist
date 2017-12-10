from django.db import models

from utils.models import AliveManager, TimeStampedModel
from account.models import User


class Word(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey('account.User', default=User.DEFAULT_PK)

    objects = models.Manager()
    alive_objects = AliveManager()
