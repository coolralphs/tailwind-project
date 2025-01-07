from django import forms
from .models import Answer, Itinerary, ItineraryDestination, ItineraryItem, Question, QuestionAnswer, UserSurvey
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, datetime
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms import formset_factory
from django.forms import inlineformset_factory

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
            'name': forms.TextInput(attrs={'style': 'width: 300px;'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['disabled'] = True
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

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
        # labels = {
        #     'country': '',  # Set an empty string to hide
        #     'city': '',  # Set an empty string to hide
        # }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) or isinstance(field, forms.IntegerField): 
                field.widget.attrs['class'] = 'form-control'
                pass     
        # itinerary = Itinerary.objects.filter(id=kwargs.pop('itinerary_id', None)).first()
        # self.fields['itinerary'].initial=itinerary
        self.fields['country'].required = False
        self.fields['city'].required = False



class ItineraryItemForm(forms.ModelForm):
    expand_item = forms.CharField(widget=forms.HiddenInput())
    destination = ItineraryDestinationForm()
    class Meta:
        model = ItineraryItem
        fields = '__all__'
        widgets = {
            'itinerary_destination': forms.Select(attrs={'class': 'form-control','style':'margin-top: 10px'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'start_time': TimePickerInput(attrs={'value': 12}),
            'end_time': TimePickerInput(attrs={'value': 13}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) or isinstance(field, forms.IntegerField): 
                field.widget.attrs['class'] = 'form-control'
                pass
            if isinstance(field, forms.BooleanField): 
                field.widget.attrs['class'] = 'form-check'
                pass
        self.fields['start_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['end_date'].widget.attrs['autocomplete'] = 'off'
        self.fields['itinerary_destination'].choices = sorted(self.fields['itinerary_destination'].choices, key=lambda x: x[1])
        # self.fields['itinerary_destination'].label = '' # Set an empty string to hide
        self.fields['itinerary_destination'].required = False

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
