# Generated by Django 4.2.16 on 2024-12-17 05:18

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_usersurvey_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=150)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_user_generated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itinerary')),
            ],
        ),
        migrations.AlterField(
            model_name='usersurvey',
            name='description',
            field=models.CharField(default=app.models.UserSurvey.get_default_desc, max_length=150),
        ),
        migrations.CreateModel(
            name='ItineraryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Transportation'), (2, 'Food & Drinks'), (3, 'Accomodation & Stays'), (4, 'Activities & Tourism'), (5, 'Other')])),
                ('place_name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('number_bought', models.IntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_skip', models.BooleanField(default=False)),
                ('is_booked', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('reservation_needed', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('rating', models.IntegerField(blank=True, choices=[(None, 'Not Rated'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], null=True)),
                ('notes', models.TextField()),
                ('itinerary_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itinerarydestination')),
            ],
        ),
        migrations.AddField(
            model_name='itinerary',
            name='user_survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usersurvey'),
        ),
    ]
