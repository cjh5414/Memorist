from __future__ import unicode_literals
from django.db import migrations
from django.contrib.auth.hashers import make_password


def forwards_func(apps, schema_editor):
    User = apps.get_model("account", "User")
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).bulk_create([
        User(username='test', password=make_password('test1234!'))
    ])


def reverse_func(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).filter(username='test').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
