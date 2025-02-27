# Generated by Django 4.2.16 on 2024-12-03 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_questionanswer_answerid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswer',
            name='AnswerId',
        ),
        migrations.RemoveField(
            model_name='questionanswer',
            name='QuestionId',
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='Answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='Question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.question'),
            preserve_default=False,
        ),
    ]
