from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from datetime import datetime
from django_countries.fields import CountryField
from django_countries import countries
import calendar

# # Create your models here.
# class User(models.Model):
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=150)

#     def __str__(self):
#         return self.first_name + " - " + self.last_name


class Answer(models.Model):
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


class Question(models.Model):
    title = models.CharField(max_length=150)
    question_text = models.CharField(max_length=150)
    is_multiple_choice = models.BooleanField(default=True)

    def __str__(self):
        return self.title + " - " + self.question_text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + " - " + self.answer.description


class UserSurvey(models.Model):
    MONTH_CHOICES = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def get_default_year():
        current_year = datetime.now().year   
        return current_year
    
    def get_default_month():
        current_month = datetime.now().month  
        return current_month
    
    def get_default_desc():
        current_month = calendar.month_name[datetime.now().month]
        current_year = datetime.now().year 

        return f"{current_month} {current_year} - Trip Helper" 

    travel_year = models.IntegerField(default=get_default_year)
    travel_month = models.IntegerField(choices=MONTH_CHOICES, default=get_default_month) 
    description = models.CharField(max_length=150, default=get_default_desc)

    def __str__(self):
        return self.description


class Itinerary(models.Model):
    name = models.CharField(max_length=150)
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_user_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.user_survey.description

def get_country_name(country):
        return countries.name(country)

class ItineraryDestination(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    country = CountryField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['itinerary', 'country', 'city'], name='unique_itinerary_country_city')
        ]

    def __str__(self):
        return f"{self.city}, {self.country}"
    
    @property
    def country_name(self):
        return get_country_name(self.country)


class ActivityType(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Activity(models.Model):
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class ItineraryItem(models.Model):
    RATING_CHOICES = [
    (None, 'Not Rated'),
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
    ]
    TYPE_CHOICES = [
    (1, 'Transportation'),
    (2, 'Food & Drinks'),
    (3, 'Accomodation & Stays'),
    (4, 'Activities & Tourism'),
    (5, 'Other'),
    ]
    itinerary_destination = models.ForeignKey(ItineraryDestination, on_delete=models.CASCADE)
    # type = models.IntegerField(choices=TYPE_CHOICES)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()    
    number_bought = models.IntegerField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_skip = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    booking_required = models.BooleanField(default=False)
    pre_payment_required = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    url = models.URLField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.start_date} {self.place_name}"

    @property
    def icon1(self):
        if self.type == 1:
            return "car"
        elif self.type == 2:
            return "utensils"
        elif self.type == 3:
            return "hotel"
        elif self.type == 4:
            return "landmark"
        elif self.type == 5:
            return "star"
        else:
            return "warning"
    @property
    def icon2(self):
        if self.type == 1:
            return "plane"
        elif self.type == 2:
            return "wine-glass"
        elif self.type == 3:
            return "bed"
        elif self.type == 4:
            return "map-pin"
        elif self.type == 5:
            return "star"
        else:
            return "warning"


class UserSurveyQuestionAnswer(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class test(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
