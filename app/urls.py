from django.urls import path, re_path
from . import views
from app.views import *

# app_name = "app"

urlpatterns = [
    path("", index, name="index"),
    path("stuff/", stuff, name="stuff"),

    path("activities/", ActivityListView.as_view(), name="activities"),

    path("answers/", AnswerListView.as_view(), name="answers"),
    path("answers/<int:pk>/update/", AnswerUpdateView.as_view(), name="update_answer"),
    path("create_answer/", AnswerCreateView.as_view(), name="create_answer"),

    path("questions/", QuestionListView.as_view(), name="questions"),
    path("questions/<int:pk>/update/", QuestionUpdateView.as_view(), name="update_question"),
    path("create_question/", QuestionCreateView.as_view(), name="create_question"),
    path("questionanswers/", QuestionAnswerListView, name="questionanswers"),
    path("create_questionanswer/", QuestionAnswerCreateView.as_view(), name="create_questionanswer"),
    path("create_question_w_answers/", create_question_w_answers, name="create_question_w_answers"),

    path("itinerary/<int:itinerary_id>/expand/<str:expand_item>/", ItineraryView, name="itinerary"),
    path("itinerary/<int:itinerary_id>/expand/", ItineraryView, name="itinerary"),
    path("itinerary/<int:itinerary_id>/", ItineraryView, name="itinerary"),
    path("itineraries/", ItineraryListView.as_view(), name="itineraries"),
    # path("itinerary/<int:itinerary_id>/add_destination/", ItineraryDestinationCreateView.as_view(), name="add_itinerary_destination"),
    path("create_itinerary/", ItineraryCreateView.as_view(), name="create_itinerary"),
    path("itinerary/<int:itinerary_id>/create_activity", ItineraryItemCreateView.as_view(), name="create_itinerary_activity"),
    path("itinerary/<int:itinerary_id>/update_activity/<int:pk>/", ItineraryItemUpdateView.as_view(), name="update_itinerary_activity"),
    # path("create_destination", ItineraryDestinationCreateView.as_view(), name="create_destination"),
    path("itinerary/<int:pk>/update/", ItineraryUpdateView.as_view(), name="update_itinerary"),

    path("survey/<int:survey_id>/question/<int:question_id>/", SurveyQuestionView, name='survey_question'),
    path("survey_complete/", survey_complete, name="survey_complete"),
    path("survey_delete/<int:survey_id>/", SurveyDeleteView, name="survey_delete"),
    path("survey_start/<int:survey_id>", SurveyStartView, name="survey_start"),
    path("survey_start/", SurveyStartView, name="survey_start"),

    path("trip_helper/", TripHelperListView, name="trip_helper"),

    path("register_user/", register_view, name="register_user"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
