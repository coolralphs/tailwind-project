from django import forms
from .models import Answer, Activity, Itinerary, ItineraryDestination, ItineraryItem, Question, QuestionAnswer, UserSurvey
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, datetime
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms import formset_factory
from django.forms import inlineformset_factory
from asgiref.sync import sync_to_async
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField
import json

class TwelveHourTimeInput(forms.TimeInput):
    input_type = 'time'
    format = '%I:%M %p'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            'description': 'Answer',
        }


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = 'user_survey','name',
        labels = {
            'user_survey': 'Trip Helper Survey',
            'name': 'Itinerary Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control left-control ', 'disabled': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autocomplete'] = 'off'


@sync_to_async
def get_itinerary(itinerary_id):
    return Itinerary.objects.get(id=itinerary_id)


class ItineraryDestinationForm(forms.ModelForm):
    destination = forms.ChoiceField(
        choices=[('existing', 'Existing'), ('new', 'New')],
        initial='existing',
        widget=forms.RadioSelect(),
        required=True
    )
    class Meta:
        model = ItineraryDestination
        fields = ['destination', 'itinerary', 'country', 'city',] 
        widgets = {
            'itinerary': forms.Select(attrs={'class': 'my-select-class'}),
            'itinerary': forms.HiddenInput(),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) or isinstance(field, forms.IntegerField): 
                field.widget.attrs['class'] = 'form-control'
                pass     
        self.fields['country'].required = False
        self.fields['city'].required = False

    async def async_init(self, *args, **kwargs):
        self.fields['itinerary'].initial = await get_itinerary(kwargs.pop('itinerary_id'))


class ItineraryItemForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    operation = forms.CharField(widget=forms.HiddenInput())
    expand_item = forms.CharField(widget=forms.HiddenInput())
    activity_array = forms.CharField( 
        widget=forms.HiddenInput(),
        required=False,
    )
    destination = ItineraryDestinationForm()
    class Meta:
        model = ItineraryItem
        fields = '__all__'
        widgets = {
            'itinerary_destination': forms.Select(attrs={'class': 'form-control','style':'margin-top: 10px'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control updatable'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control updatable'}),
            'start_time': forms.TextInput(attrs={'class': 'form-control updatable'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control updatable'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) or isinstance(field, forms.IntegerField): 
                field.widget.attrs['class'] = 'form-control updatable'
                pass
            if isinstance(field, forms.BooleanField): 
                field.widget.attrs['class'] = 'form-check'
                pass
        self.fields['start_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['end_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['place_name'].widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['autocomplete'] = 'off'
        self.fields['itinerary_destination'].choices = sorted(self.fields['itinerary_destination'].choices, key=lambda x: x[1])
        self.fields['itinerary_destination'].required = False
        self.fields['expand_item'].required = False
        
        self.fields['operation'].required = False
        self.fields['id'].required = False

        data = Activity.objects.all()
        data_list = data.values_list('activity_type_id', 'id', 'name').annotate(
            custom_order=Case(
                When(name="Other", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('custom_order','name')
        activity_array = json.dumps(list(data_list))
        self.fields['activity_array'].initial = activity_array

# MyFormSet = formset_factory(ItineraryItemForm, extra=2)
# ItineraryItemFormSet = inlineformset_factory(ItineraryDestination,ItineraryItem, 
#                                             form=ItineraryItemForm, extra=1)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            "question_text": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            'question_text': 'Question',
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-Mail")    

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError("A user with that email address already exists.")
    

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        is_multiple_choice = kwargs.pop('is_multiple_choice', False) 
        super().__init__(*args, **kwargs)
        data= QuestionAnswer.objects.all()
        CHOICES = []
        for i in data: 
            CHOICES.append((i.answer.id, i.answer.description))
        if is_multiple_choice:
            self.fields['answers'] = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple,label="Select options:")
        else:
            self.fields['answers'] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Select only one:")

class UserSurveyForm(forms.ModelForm):
    class Meta:
        model = UserSurvey
        fields = ['travel_month','travel_year','description']
        labels = {
            'travel_month': 'Month',
            'travel_year': 'Year',
            'description': 'Trip Name'
        }
        widgets = {
            'description': forms.TextInput(attrs={'readOnly': True}),
        }

    def clean_travel_year(self):
        year = self.cleaned_data['travel_year']
        current_year = datetime.now().year
        if (year < current_year):            
            raise forms.ValidationError(f"Year can't be less than {current_year}.")
        return year
