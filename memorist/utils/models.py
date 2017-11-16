from django.db import models


class AliveManager(models.Manager):
    def get_queryset(self):
        return super(AliveManager, self).get_queryset().filter(is_delete=False)
