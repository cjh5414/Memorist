from django.db import models

from utils.models import AliveManager, TimeStampedModel
from account.models import User


class Word(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    QUESTION_TYPES = (
        ('W', 'Words'),
        ('S', 'Sentences')
    )
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES, default='W')
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey('account.User', default=User.DEFAULT_PK)

    objects = models.Manager()
    alive_objects = AliveManager()

    def __str__(self):
        return '%s %s %s %s %s'\
               % (self.question, self.answer, self.question_type, self.is_deleted, self.user.username)
