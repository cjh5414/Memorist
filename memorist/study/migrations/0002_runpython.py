from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    User = apps.get_model("account", "User")
    Study = apps.get_model("study", "Study")
    for user in User.objects.all():
        Study.objects.create(user=user)


def reverse_func(apps, schema_editor):
    Study = apps.get_model("study", "Study")
    db_alias = schema_editor.connection.alias
    Study.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
