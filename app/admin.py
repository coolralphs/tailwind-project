from django.contrib import admin
from app.models import Answer, Question, QuestionAnswer, UserSurvey, Itinerary, ItineraryDestination, ItineraryItem
# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(UserSurvey)
admin.site.register(Itinerary)
admin.site.register(ItineraryDestination)
admin.site.register(ItineraryItem)