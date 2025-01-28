from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from collections import defaultdict
from app.models import *
from django.views.generic import ListView, CreateView, UpdateView
from .forms import AnswerForm, ItineraryForm, ItineraryItemForm, QuestionForm, SurveyForm, RegisterForm, UserSurveyForm
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import inlineformset_factory
from django.db import IntegrityError
import calendar

def index(request):
    user = request.user
    if user.is_authenticated:
        # User is logged in
        username = user.username
        (f"/survey/{id}")
        context = {"message": f"Hello {username}, welcome to Tailwind Travel!"}
        pass
    else:
        context = {"message": f"Welcome to Tailwind Travel!"}
        pass
    return render(request, "index.html", context)


def stuff(request):
    return HttpResponse("Hello, world. You're at the app stuff.")

def test(request):
    form = Itinerary.objects.all()
    return render(request, 'test.html', {'form': form })

def survey_complete(request):
    context = {"message": "Thank you for completing the survey!"}
    return render(request, "survey_complete.html", context)


class ActivityListView(ListView):
    model = Activity
    template_name = "activity_list.html"


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = "create_answer.html"
    success_url = "/questionanswers/"


class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = "update_answer.html"
    success_url = reverse_lazy("questionanswers")


class AnswerListView(ListView):
    model = Answer
    template_name = "answer_list.html"


@method_decorator(login_required, name='dispatch')
class ItineraryListView(ListView):
    # model = Itinerary
    template_name = "itinerary_list.html"
    # context_object_name = 'itineraries'

    def get_queryset(self):
        return None # Not needed, as data is passed via context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itinerary_list'] = Itinerary.objects.all()
        context['itinerary_destination_list'] = ItineraryDestination.objects.all()
        return context


@login_required(login_url="/login/")
def ItineraryView(request, itinerary_id, expand_item=None):

    address_field_list = ['house_number', 'street', 'city', 'state', 'postal_code', 'country']

    if request.method == 'POST':

        # ajax call
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print('ajax')
            form = ItineraryForm(request.POST)
            if form.is_valid():
                print('valid ajax')
                itinerary = Itinerary.objects.get(id = itinerary_id)
                itinerary.name = request.POST.get('name')
                itinerary.save()
                return JsonResponse({'message': 'Itinerary name successfully updated.'})
            else:
                print('invalid ajax')
                errors = form.errors
                for i in errors:
                    print (i)
                return JsonResponse({'message': 'Itinerary name change was unsuccessful.'})
            
        else:
            pass

        form = ItineraryItemForm(data=request.POST)
        
        op = 'create'
        if form.is_valid():
            print('form valid')
            op = request.POST.get('operation')
            if op == 'create':
                print('create')
                form.save() 
                pass
            else:
                print('enter update')
                #update
                id = form.cleaned_data['id']                
                item = ItineraryItem.objects.get(id=id)
                # item.itinerary_destination = form.cleaned_data['itinerary_destination']
                # item.activity_type = form.cleaned_data['activity_type']
                # item.activity = form.cleaned_data['activity']
                item.place_name = form.cleaned_data['place_name']

                item.osm_key = form.cleaned_data['osm_key']
                item.osm_value = form.cleaned_data['osm_value']
                item.house_number = form.cleaned_data['house_number']
                item.street = form.cleaned_data['street']
                item.city = form.cleaned_data['city']
                item.state = form.cleaned_data['state']
                item.postal_code = form.cleaned_data['postal_code']
                item.country = form.cleaned_data['country']
                item.latitude = form.cleaned_data['latitude']
                item.longitude = form.cleaned_data['longitude']

                item.description = form.cleaned_data['description']
                item.start_date = form.cleaned_data['start_date']
                item.end_date = form.cleaned_data['end_date']
                item.start_time = form.cleaned_data['start_time']
                item.end_time = form.cleaned_data['end_time']     
                item.number_bought = form.cleaned_data['number_bought']
                item.total_cost = form.cleaned_data['total_cost']
                item.is_skip = form.cleaned_data['is_skip']
                item.is_booked = form.cleaned_data['is_booked']
                item.booking_required = form.cleaned_data['booking_required']
                item.pre_payment_required = form.cleaned_data['pre_payment_required']
                item.is_paid = form.cleaned_data['is_paid']
                item.url = form.cleaned_data['url']
                item.rating = form.cleaned_data['rating']
                item.notes = form.cleaned_data['notes']               

                item.save()
                pass
        else:
            print('not valid')
            errors = form.errors
            for i in errors:
                print (i)
                
            print(request.POST.getlist('start_time'))
            destinations = ItineraryDestination.objects.filter(itinerary_id=itinerary_id).order_by("country", "city")
            itinerary = Itinerary.objects.filter(id=itinerary_id).first()

            item_list = []
            unassigned_list = []
            distinct_cities = []
            grouped_dates = defaultdict(list)

            for dest in destinations:
                items = ItineraryItem.objects.filter(itinerary_destination=dest).order_by('start_date')
                if items:
                    for activity in items:
                        grouped_dates[activity.start_date].append(activity)
                        # if activity.itinerary_destination not in distinct_cities:
                        #     distinct_cities.append(activity.itinerary_destination)
                else:
                    unassigned_list.append(dest)     

            for u in unassigned_list:
                distinct_cities.append(u)

            sorted_dict = dict(sorted(grouped_dates.items()))
            form = ItineraryItemForm(initial= {'expand_item': expand_item})
            # form_destination = ItineraryDestinationForm()
            form_update_itinerary = ItineraryForm(initial= {'name': itinerary.name, 'user_survey': itinerary.user_survey})

            user_survey_id = 0
            if itinerary.user_survey:
                user_survey_id = itinerary.user_survey.id
            context = {                
                "form": form,
                # "form_destination": form_destination,
                "form_update_itinerary": form_update_itinerary,
                "grouped_dates": dict(sorted_dict),
                "distinct_cities": distinct_cities,
                "itinerary_id": itinerary_id,
                "user_survey_id" : user_survey_id,
                "itinerary_name": itinerary.name,
                "address_field_list": address_field_list,
            }
            return render(request, "itinerary.html", context)

        # form_dest = ItineraryDestinationForm(request.POST)

        # if form_dest.is_valid():
        #     if op == 'create':
        #         print('enter create')
        #         radio_selection = form_dest.cleaned_data['destination']
        #         if radio_selection == 'new':
        #             city = form_dest.cleaned_data['city']
        #             country = form_dest.cleaned_data['country']
        #             itinerary = Itinerary.objects.get(id=itinerary_id)
        #             #save to db, then pass new itinerary_destination below
        #             itin_dest = ItineraryDestination.objects.create(itinerary=itinerary, city=city, country=country)
        #             action = form.save(commit=False)
        #             action.itinerary_destination = itin_dest
        #             try:
        #                 action.save()
        #             except IntegrityError as e:
        #                 # Handle the integrity error (e.g., duplicate key, etc.)
        #                 print("IntegrityError:", e)
        #             except Exception as e:
        #                 # Handle other potential exceptions
        #                 print("Error saving model:", e)

        #             pass
        #         else:                
        #             form.save()
        #     else:
        #         print('enter update')
        #         #update
        #         id = form.cleaned_data['id']                
        #         item = ItineraryItem.objects.get(id=id)
        #         item.itinerary_destination = form.cleaned_data['itinerary_destination']
        #         item.activity_type = form.cleaned_data['activity_type']
        #         item.activity = form.cleaned_data['activity']
        #         item.place_name = form.cleaned_data['place_name']
        #         item.description = form.cleaned_data['description']
        #         item.start_date = form.cleaned_data['start_date']
        #         item.end_date = form.cleaned_data['end_date']
        #         item.start_time = form.cleaned_data['start_time']
        #         item.end_time = form.cleaned_data['end_time']     
        #         item.number_bought = form.cleaned_data['number_bought']
        #         item.total_cost = form.cleaned_data['total_cost']
        #         item.is_skip = form.cleaned_data['is_skip']
        #         print(form.cleaned_data['is_skip'])
        #         item.is_booked = form.cleaned_data['is_booked']
        #         item.booking_required = form.cleaned_data['booking_required']
        #         item.pre_payment_required = form.cleaned_data['pre_payment_required']
        #         item.is_paid = form.cleaned_data['is_paid']
        #         item.url = form.cleaned_data['url']
        #         item.rating = form.cleaned_data['rating']
        #         item.notes = form.cleaned_data['notes']               

        #         item.save()
        #         pass
        # else:
        #     print('form_dest NOT valid')
        #     # return
        #     pass
        
        date = form.cleaned_data['expand_item']
        return HttpResponseRedirect(f"/itinerary/{itinerary_id}/expand/{date}")
    
    else:

        # destinations = ItineraryDestination.objects.filter(itinerary_id=itinerary_id).order_by("country", "city")
        itinerary = Itinerary.objects.get(id=itinerary_id)
        items = ItineraryItem.objects.filter(itinerary=itinerary).order_by('start_date')
        unassigned_list = []
        # distinct_cities = []
        grouped_dates = defaultdict(list)

        if items:
            for activity in items:
                grouped_dates[activity.start_date].append(activity)
                # if activity.itinerary_destination not in distinct_cities:
                #     distinct_cities.append(activity.itinerary_destination)    

        # for dest in destinations:
        #     items = ItineraryItem.objects.filter(itinerary_destination=dest).order_by('start_date')
        #     if items:
        #         for activity in items:
        #             grouped_dates[activity.start_date].append(activity)
        #             if activity.itinerary_destination not in distinct_cities:
        #                 distinct_cities.append(activity.itinerary_destination)
        #     else:
        #         unassigned_list.append(dest)     

        # for u in unassigned_list:
        #     distinct_cities.append(u)

        sorted_dict = dict(sorted(grouped_dates.items()))
        for i in sorted_dict:
            print(i)
        form = ItineraryItemForm(initial= {'expand_item': expand_item, 'itinerary': itinerary})
        # form_destination = ItineraryDestinationForm()
        form_update_itinerary = ItineraryForm(initial= {'name': itinerary.name, 'user_survey': itinerary.user_survey})

        user_survey_id = 0
        if itinerary.user_survey:
            user_survey_id = itinerary.user_survey.id

        map_center = (40.7128, -74.0060)
        map_zoom = 12

        context = {
            # "formset": formset,
            "form": form,
            # "form_destination": form_destination,
            "form_update_itinerary": form_update_itinerary,
            "grouped_dates": dict(sorted_dict),
            # "distinct_cities": distinct_cities,
            "itinerary_id": itinerary_id,
            "user_survey_id" : user_survey_id,
            "itinerary_name": itinerary.name,
            "itinerary": itinerary,
            "map_center": map_center,
            "map_zoom": map_zoom,
            "address_field_list": address_field_list,
        }
    return render(request, "itinerary.html", context)


@method_decorator(login_required, name='dispatch')
class ItineraryItemCreateView(CreateView):
    model = ItineraryItem
    form_class = ItineraryItemForm
    template_name = "create_itinerary_activity.html"

    def get_success_url(self):
        return reverse_lazy('itinerary', kwargs={'itinerary_id': self.kwargs['itinerary_id']})

    # def get_form(self, form_class=None):
    #     id = self.kwargs.get('itinerary_id') 
    #     itinerary = Itinerary.objects.get(id=id)
    #     CHOICES = []
    #     data = ItineraryDestination.objects.filter(itinerary=itinerary).order_by('city')
    #     for i in data:
    #         CHOICES.append((i.id, i))
    #     form = super().get_form(form_class)
    #     form.fields['itinerary_destination'].choices = CHOICES
    #     return form


@method_decorator(login_required, name='dispatch')
class ItineraryItemUpdateView(UpdateView):
    model = ItineraryItem
    form_class = ItineraryItemForm
    template_name = "update_itinerary_activity.html"

    def get_success_url(self):
        return reverse_lazy('itinerary', kwargs={'itinerary_id': self.kwargs['itinerary_id']})

class ItineraryCreateView(CreateView):
    model = Itinerary    
    form_class = ItineraryForm
    template_name = "create_itinerary.html"
    success_url = "/itineraries/"


class ItineraryUpdateView(UpdateView):
    model = Itinerary
    form_class = ItineraryForm
    template_name = "update_itinerary.html"

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('itinerary', kwargs={'itinerary_id': pk})


def custom_sort_key(product):
    # Define your custom sorting logic here
    return product.price * 2

# class ItineraryDestinationCreateView(CreateView):
#     model = ItineraryDestination
#     form_class = ItineraryDestinationForm
#     template_name = "create_destination.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         itinerary_id = self.kwargs['itinerary_id']
#         context['itinerary_id'] = itinerary_id
#         # itinerary = Itinerary.objects.get(id=itinerary_id)
#         return context 

#     def get_success_url(self):
#         return reverse_lazy('itinerary', kwargs={'itinerary_id': self.kwargs['itinerary_id']})


class Itin:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


@login_required(login_url="/login/")
def TripHelperListView(request):
    data = UserSurvey.objects.filter(user=request.user).order_by("-is_complete", "travel_year", "travel_month")
    q_first = Question.objects.order_by('id').first()

    new_list = defaultdict(list)
    suggested_list = defaultdict(list)
    approved_list = defaultdict(list)

    if q_first:
        pass
    else:
        context = {"message": "No questions are set up to start itinerary helper."}
        return render(request, "trip_helper.html", context)
        pass

    for item in data:
        itins = Itinerary.objects.filter(user_survey=item)
        if itins:
            for i in itins:
                key_object = Itin(item.id, item.description)
                suggested_list[key_object].append(i)
                # suggested_list[item.description].append(i)
                # pass
        else:
            new_list[item].append(item)
            # pass

    context = {
        "new_list": dict(new_list),
        "suggested_list": dict(suggested_list),
        "approved_list": dict(approved_list),
        "question_id": q_first.id
    }
    return render(request, "trip_helper.html", context)


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "create_question.html"
    success_url = reverse_lazy("questionanswers")


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "update_question.html"
    success_url = reverse_lazy("questionanswers")


class QuestionListView(ListView):
    model = Question
    template_name = "question_list.html"


class QuestionAnswerCreateView(CreateView):
    model = QuestionAnswer
    fields = ["question", "answer"]
    template_name = "create_questionanswer.html"
    success_url = "/questionanswers/"


def QuestionAnswerListView(request):
    data = QuestionAnswer.objects.all()
    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item.question].append(item)

    context = {"grouped_data": dict(grouped_data)}
    return render(request, "questionanswer_list.html", context)


@login_required(login_url="/login/")
def SurveyQuestionView(request, survey_id=None, question_id=None):
    q_first = Question.objects.order_by('id').first()
    q_last = Question.objects.order_by('-id').first()
    question = Question.objects.filter(id=question_id).first()

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            
            # checked_values = form.cleaned_data['answers']
            checked_values = request.POST.getlist('answers')
            survey = UserSurvey.objects.filter(user=request.user, id=survey_id).first()
            existing_answers = UserSurveyQuestionAnswer.objects.filter(user_survey=survey, question=question)

            for answer in existing_answers:
                answer.delete()
                
            for answer_id in checked_values:
                question = Question.objects.filter(id=question_id).first()
                answer = Answer.objects.filter(id=answer_id).first()
                UserSurveyQuestionAnswer.objects.create(user_survey=survey, question=question, answer=answer)

            if question_id == q_last.id:
                survey = UserSurvey.objects.filter(user=request.user, id=survey_id).first()
                survey.is_complete = True
                survey.save()
                context = {"message": "Thank you, you have completed the survey!"}
                return render(request, "survey_complete.html", context)

            else:
                question_id += 1
                return HttpResponseRedirect(f"/survey/{survey_id}/question/{question_id}")
        else:
            data = QuestionAnswer.objects.filter(question_id=question_id)
            CHOICES = []
            for i in data:
                CHOICES.append((i.answer.id, i.answer.description))
            form = SurveyForm()
            form.fields['answers'].choices = CHOICES
            return render(request, 'survey.html', {'form': form, 'question': question, 'current_id':question_id, 'survey_id': survey_id, 'first_id':q_first.id, 'last_id':q_last.id, 'error':'*This field is required' })
    else:        
        if q_first:
            pass
        else:
            context = {"message": f"No questions are set up to start itinerary helper."}
            return render(request, "index.html", context)
            pass
        
        if UserSurvey.objects.filter(id=survey_id).exists():            
            pass
        else:
            return redirect('survey_start')

        existing_question = Question.objects.filter(id=question_id).first()
        if existing_question:
            pass
        if Question.objects.filter(id=question_id).exists():
            pass
        else:
            first_id = q_first.id
            return HttpResponseRedirect(f"/survey/{survey_id}/question/{first_id}")
            
        survey = UserSurvey.objects.filter(user=request.user, id=survey_id).first()

        data = QuestionAnswer.objects.filter(question_id=question_id)
        
        CHOICES = []
        initial_values = []
        for i in data:
            CHOICES.append((i.answer.id, i.answer.description))        
            existing_answers = UserSurveyQuestionAnswer.objects.filter(user_survey=survey, question=i.question, answer=i.answer)

            for a in existing_answers:
                initial_values.append(a.answer_id)

        form = SurveyForm(initial= {'answers': initial_values}, is_multiple_choice=existing_question.is_multiple_choice)
        form.fields['answers'].choices = CHOICES

    return render(request, "survey.html", {'form': form, 'question': question, 'current_id':question_id, 'survey_id': survey_id, 'first_id':q_first.id, 'last_id':q_last.id })


@login_required(login_url="/login/")
def SurveyStartView(request, survey_id=None):
    if request.method == 'POST':
        form = UserSurveyForm(request.POST)
        if form.is_valid():
            travel_month = form.cleaned_data['travel_month']
            travel_year = form.cleaned_data['travel_year']
            description = form.cleaned_data['description']

            user_survey = UserSurvey.objects.filter(user=request.user, id=survey_id).first()
            next_id = 0
            if user_survey:
                #update existing
                user_survey.travel_month = travel_month
                user_survey.travel_year = travel_year
                user_survey.description = description
                user_survey.save()
                next_id = user_survey.id

                pass
            else:
                #add new
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                next_id = post.id
                pass

            q_first = Question.objects.order_by('id').first()
            if q_first:
                return HttpResponseRedirect(f"/survey/{next_id}/question/{q_first.id}")
            else:
                context = {"message": "There are no questions to answer!"}
                return render(request, "survey_complete.html", context)
        else:
            print('not valid')    
            errors = form.errors
            for i in errors:
                print (i)
            return render(request, "survey_update.html", {'form': form})
    else:
        if survey_id:
            user_survey = UserSurvey.objects.filter(user=request.user, id=survey_id).first()
            form = UserSurveyForm(initial= {
                'travel_year': user_survey.travel_year, 
                'travel_month': user_survey.travel_month,
                'description': user_survey.description
            })
            return render(request, "survey_update.html", {'form': form})
        else:
            exist = QuestionAnswer.objects.first()
            if exist:
                form = UserSurveyForm()
                return render(request, "survey_update.html", {'form': form})
            else:
                context = {"message": "There are no questions set up in this survey!"}
                return render(request, "survey_update.html", context)
            


def SurveyDeleteView(request, survey_id):
    survey = UserSurvey.objects.filter(user=request.user, id = survey_id).first()
    if request.method == 'POST':
        if survey:
            survey.delete()
            return redirect('trip_helper')
        else:
            return render(request, 'survey_delete.html', {'form': form })        
    else:
        form = survey
        return render(request, 'survey_delete.html', {'form': form }) 


def create_question_w_answers(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        question_text = request.POST.get('question_text')

        # Create the question
        question = Question.objects.create(title=title, question_text=question_text)

        # Get the answers from the form
        answers = request.POST.getlist('answer')

        # Create comments for each comment entered
        for description in answers:
            answer = Answer.objects.create(description=description)
            QuestionAnswer.objects.create(question=question, answer=answer)

        return redirect('questionanswers')

    return render(request, 'create_question_w_answers.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            context = {"message": "Registration successful! Welcome to Tailwind Travel!"}
            return render(request, "index.html", context)
        else:
            print(form.errors)
            errors = form.errors
            return render(request, 'register_user.html', {'form': form })
    else:
        form = RegisterForm()
        # form = RegisterForm()
        return render(request, "register_user.html", { "form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                print(request.POST.get('next'))
                return redirect(request.POST.get('next'))
                # return HttpResponseRedirect(request.POST.get('next'))
            else:
                print(request.POST.get('next'))
                return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", { "form": form})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", { "form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        context = {"message": "You have successfully logged out."}
        return render(request, "index.html", context)