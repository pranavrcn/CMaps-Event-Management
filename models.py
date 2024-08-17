from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django import forms
from address.models import AddressField
# from .forms import EVENT_CATEGORIES
import datetime
from datetime import date
from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User


    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    interaction_value = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)



# model to save values of organization request
class RegistrationRequest(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    public_org = models.BooleanField(default=True)
    contact_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    profile_pic = models.ImageField(default="profile_picture/usericon.png", null=True, blank=True, upload_to="profile_picture/")
    friends = models.ManyToManyField("Member", null=True, blank=True)
    organizations = models.ManyToManyField("Organization", blank=True)
    new_user = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    

class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        Member, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        Member, related_name="to_user", on_delete=models.CASCADE)

    def __str__(self):
        return "From: " + str(self.from_user) + "\n" + "To: " + str(self.to_user)

class Organization_Request(models.Model):
    from_user = models.ForeignKey(
        Member, on_delete=models.CASCADE)
    to_org = models.ForeignKey(
        "Organization", on_delete=models.CASCADE)
    
class Organization_Invite(models.Model):
    from_org = models.ForeignKey(
        "Organization", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        Member, on_delete=models.CASCADE)
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    tags = models.CharField(max_length=255)

class UserAnalytics(models.Model):
    INTERACTION_CHOICES = [
        ('view', 'View'),
        ('save', 'Save'),
        ('attendance', 'Attendance'),
    ]
    
# EVENT_ICONS = {
#     "SP": "Sports-outlined.png",
#     "CO": "CIO-outlined.png",
#     "CR": "Career-outlined.png",
#     "OT": "Misc. Marker.png",
#     "UV": "UVA-Marker.png",
#     "FD": "Food Marker.png",
#     "SC": "Social-Marker.png",
# }

EVENT_ICONS = {
    "SP": "Sports-outlined1.png",
    "CO": "CIO-outlined1.png",
    "CR": "Career-outlined5.png",
    "OT": "Misc-Marker1.png",
    "UV": "UVA-Marker5.png",
    "FD": "Food-Marker1.png",
    "SC": "Social-Marker1.png",
}

EVENT_CATEGORIES = [
    ("UV", "UVA"),
    ("CO", "CIO"),
    ("SP", "Sports"),
    ("CR", "Career"),
    ("SC", "Social"),
    ("FD", "Food"),
    ("OT", "Other"),
]

EVENT_TAGS = [
    ("FS", "Free Swag"),
    ("VI", "Virtual"),
    ("RF", "Raffles"),
    ("UG", "Undergraduate"),
    ("GR", "Graduate"),
    ("MU", "Music"),
    ("DN", "Dancing"),
    ("HW", "Health & Wellness"),
]

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=EVENT_CATEGORIES, default="OT")
    description = models.TextField(max_length=500)
    address = AddressField(default=None)
    address_details = models.CharField(null=True, blank=True, max_length=50)
    public_event = models.BooleanField(default=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    event_image = models.ImageField(default="", null=True, blank=True, upload_to="events-pictures/")
    interested_members = models.ManyToManyField(Member, null=True, blank=True)
    RSVP_link = models.CharField(max_length=200, null=True, blank=True, default=None)

    def __str__(self):
        return self.event_name
    
    def getOrganizerImage(self):
        try:
            org = Organization.objects.get(user=self.organizer)
            return org.org_image.url
        except:
            membr = Member.objects.get(user=self.organizer)
            return membr.profile_pic.url
    
    def getIMCount(self):
        temp = list(self.interested_members.all())
        return len(temp)
    
    def getOrganizerName(self):
        try:
            temp = Organization.objects.get(user=self.organizer)
            return str(temp.name)
        except:
            temp = Member.objects.get(user=self.organizer)
            return str(temp)
        
    def getEventIcon(self):
        return "/media/events-pictures/" + EVENT_ICONS[self.category]
    
    # return whether the event is today or not
    def isToday(self):
        return self.start_time.date() == date.today()
    
    def testFunction(self, data):
        return data
    
    def all_day(self):
        return (self.start_time.time() == self.end_time.time()) and (self.start_time.time() == datetime.time(hour=0, minute=0, second=0))

class MemberInfo(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    member_interest = models.TextField(max_length=500)
    where_from = models.TextField(max_length=100)
    


class FeedBack(models.Model):
    feedback_info = models.TextField(max_length=500)
    user_feedback = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    datetime_feedback = models.DateTimeField(blank=True)

    def __str__(self):
        return self.feedback_info

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    members = models.ManyToManyField(Member, default=None, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    org_image = models.ImageField(default="images/orglogo.jpg", null=True, blank=True, upload_to="images/")
    public_org = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class DataSerializer(serializers.ModelSerializer):

    full_address = serializers.SerializerMethodField()

    class Meta:
        model=Event
        fields=('event_name',
                'category', 
                'description', 
                'full_address', 
                'address_details', 
                'public_event',
                'organizer',
                'start_time',
                'end_time',
                'RSVP_link')

    def get_full_address(self, obj):
        address_obj = obj.address
        if address_obj:
            return str(address_obj)
            print(address_obj)
            return {
                'street': address_obj.street,
                'city': address_obj.city,
                'state': address_obj.state,
                'zip_code': address_obj.zip_code,
                # Add more fields if necessary
            }
        else:
            return None

from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    # if instance:
    if created and instance.first_name:
        Member.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
