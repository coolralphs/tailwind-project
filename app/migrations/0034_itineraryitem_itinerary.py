# Generated by Django 4.2.16 on 2025-01-27 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_itineraryitem_osm_key_itineraryitem_osm_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='itineraryitem',
            name='itinerary',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.itinerary'),
            preserve_default=False,
        ),
    ]
