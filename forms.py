from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django import forms
from address.forms import AddressField
import datetime
from .models import Member, EVENT_CATEGORIES, EVENT_TAGS
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm
from .views import Organization, RegistrationRequest

class OrganizationRegistration(forms.ModelForm):
    confirm_password=forms.CharField(max_length=32, widget=forms.PasswordInput())
    class Meta:
        model = RegistrationRequest
        fields = ["name", "description", "public_org", "contact_email", "username", "password"]
        widgets = {
            "password": forms.PasswordInput
        }
        labels = {
            "name": "Organization Name",
            "description": "Organization Description",
            "public_org": "Is this a public organization?",            
        }

    def clean(self):
        cleaned_data = super(OrganizationRegistration, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )


WHERE_FROM = [
    ("YY", "YikYak"),
    ("IG", "Instagram"),
    ("RD", "Reddit"),
    ("OT", "Other"),
]



class InterestForm(forms.Form):
    interests = forms.MultipleChoiceField(required=False,
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=EVENT_TAGS)
    where_from = forms.MultipleChoiceField(required=True,
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=WHERE_FROM)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.Form):
    image_upload = forms.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg',
                                                                                           'png',
                                                                                           'jpeg',
                                                                                           'svg',
                                                                                           ])])

    
class OrganizationProfileForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=200)
    public_org = forms.BooleanField()
    image_upload = forms.ImageField(required=False)

class FeedBackForm(forms.Form):
    feedback_info = forms.CharField(widget=forms.Textarea, max_length=500)
    class Meta:
        labels = {
            "feedback_info": "Feedback",         
        }
    

class EventCreation(forms.Form):
    event_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, max_length=500)
    category = forms.ChoiceField(choices=EVENT_CATEGORIES)
    address = AddressField()
    address_details = forms.CharField(required=False, max_length=50, label="Room (optional)")
    public_event = forms.BooleanField(required=False)
    # event_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget)
    start_time = forms.DateTimeField(initial=datetime.date.today, 
                                     widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    end_time = forms.DateTimeField(initial=datetime.date.today, 
                                   widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    event_image = forms.ImageField(required=False)
    RSVP_link = forms.CharField(max_length=200, required=False)

class EventSearch(forms.Form):
    search_param = forms.CharField(max_length=50, required=False)
    category = forms.MultipleChoiceField(required=False,
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=EVENT_CATEGORIES)
    # today, this week, this month -- possibly
    