from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable


class User(AbstractUser):
    name = models.CharField(null=False, max_length=30)
    email = models.EmailField(null=False, max_length=254)


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)
