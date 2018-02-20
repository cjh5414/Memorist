from __future__ import unicode_literals
from django.db import migrations


def forwards_func(apps, schema_editor):
    Word = apps.get_model("wordlist", "Word")

    db_alias = schema_editor.connection.alias
    Word.objects.using(db_alias).bulk_create([
        Word(question='책', answer='book', user_id=2),
        Word(question='book', answer='책', user_id=2),
        Word(question='컵', answer='cup', user_id=2, is_deleted=True),
        Word(question='안경', answer='glasses', user_id=2, is_deleted=True),
        Word(question='나는 학생입니다', answer='I am a student.', user_id=2),
        Word(question='im not going to go school tomorrow.', answer='나는 내일 학교에 가지 않을 것이다.', user_id=2),
        Word(question='오늘은 수요일이야', answer='Today is Wednesday.', user_id=2, is_deleted=True),
    ])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('wordlist', '0005_word_user'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
