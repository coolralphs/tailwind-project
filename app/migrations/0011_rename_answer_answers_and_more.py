# Generated by Django 4.2.16 on 2024-12-04 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_user_delete_person_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Answer',
            new_name='Answers',
        ),
        migrations.RenameModel(
            old_name='QuestionAnswer',
            new_name='QuestionAnswers',
        ),
        migrations.RenameModel(
            old_name='Question',
            new_name='Questions',
        ),
        migrations.RenameModel(
            old_name='User',
            new_name='Users',
        ),
    ]
