from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Study.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.study.save()
