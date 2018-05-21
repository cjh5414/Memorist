from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    User = apps.get_model("account", "User")
    StudyStatus = apps.get_model("studystatus", "StudyStatus")
    for user in User.objects.all():
        StudyStatus.objects.create(user=user)


def reverse_func(apps, schema_editor):
    StudyStatus = apps.get_model("studystatus", "StudyStatus")
    db_alias = schema_editor.connection.alias
    StudyStatus.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('studystatus', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
