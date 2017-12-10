from __future__ import unicode_literals
from django.db import migrations
from django.contrib.auth.hashers import make_password


def forwards_func(apps, schema_editor):
    User = apps.get_model("account", "User")
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).bulk_create([
        User(username='test', password=make_password('test1234!'), name='testname', email='cjh5414@gmail.com'),
        User(username='test2', password=make_password('test1234!'), name='testname2', email='test2@gmail.com')
    ])


def reverse_func(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).filter(username='test').delete()
    User.objects.using(db_alias).filter(username='test2').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
