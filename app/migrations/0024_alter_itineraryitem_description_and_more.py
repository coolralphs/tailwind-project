# Generated by Django 4.2.16 on 2024-12-18 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_itinerarydestination_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraryitem',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='itineraryitem',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='itineraryitem',
            name='number_bought',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='itineraryitem',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='itineraryitem',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
