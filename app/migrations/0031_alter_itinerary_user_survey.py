# Generated by Django 4.2.16 on 2025-01-15 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_activitytype_remove_itineraryitem_type_activity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='user_survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.usersurvey'),
        ),
    ]
