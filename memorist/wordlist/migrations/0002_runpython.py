from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    Word = apps.get_model("wordlist", "Word")

    db_alias = schema_editor.connection.alias
    Word.objects.using(db_alias).bulk_create([
        Word(question='사과', answer='apple'),
        Word(question='바나나', answer='banana'),
        Word(question='기억', answer='memory'),
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('wordlist', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
