from django.db import models
from utils.models import TimeStampedModel


class Study(TimeStampedModel):
    ALL_DAYS = -1
    QUESTION_TYPES = (
        ('A', 'All'),
        ('W', 'Words'),
        ('S', 'Sentences')
    )
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES, default='A')
    chosen_days = models.IntegerField(default=ALL_DAYS)
