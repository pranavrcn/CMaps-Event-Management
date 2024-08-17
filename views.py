from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.http import HttpResponseNotFound
import random
from django.conf import settings
from django.utils import timezone
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

TIME_DELTA = 7


from django.shortcuts import render
from rest_framework.response import Response
# from rest_framework.decorators import api\_view
# from .models import Data
# from .serializer import DataSerializer

# Create your views here.
@api_view(['GET'])
def API(request):
    app = Event.objects.filter(public_event=True)
    serializer = DataSerializer(app, many=True)
    return Response(serializer.data)

def mediaFolder(request):
    filepath = settings.MEDIA_ROOT
    file_list = os.listdir(filepath)

    return render(request, "mediaFolder.html", {"media_files": file_list})

def registerOrg(request):
    context = {
        
    }
    if request.method == "POST":
        form = OrganizationRegistration(request.POST)
        context['form'] = form
        if form.is_valid():
            rr = RegistrationRequest()
            rr.username = form.cleaned_data["username"]
            rr.password = form.cleaned_data["password"]
            rr.name = form.cleaned_data["name"]
            rr.description = form.cleaned_data["description"]
            rr.public_org = form.cleaned_data["public_org"]
            rr.contact_email = form.cleaned_data["contact_email"]
            rr.save()
            context["success"] = True
            return render(request, "success.html", context)        
    else:
        form = OrganizationRegistration()

    context['form'] = form
    return render(request, "registration.html", context)


@login_required
def testAjax(request):
    if request.method == 'GET':
        return HttpResponse(Event.objects.all())
    return HttpResponse("An error has occurred...")

# @login_required
def saveEvent(request):
    print('saving event')
    if request.method == 'GET':
        eventID = request.GET["post_id"]
        event = Event.objects.get(id=eventID)
        # add user to organization
        membr = Member.objects.get(user=request.user)
        int_members = event.interested_members.all()
        if membr in int_members:
            # remove them
            event.interested_members.remove(membr)
            event.save()
            return HttpResponse("removed")
        event.interested_members.add(membr)
        event.save()
        return HttpResponse("added")
    return HttpResponse("An error has occurred...")


@login_required
def addMember(request):
    if request.method == 'GET':
        userID = request.GET["post_id"]
        # add user to organization
        org = Organization.objects.get(user=request.user)
        membr = Member.objects.get(id=userID)
        org.members.add(membr)
        membr.organizations.add(org)
        membr.save()
        org.save()

        o_req = Organization_Request.objects.get(from_user=membr, to_org=org)
        o_req.delete()
        return HttpResponse("Success!")
    return HttpResponse("An error has occurred...")

@login_required
def removeMember(request):
    
    if request.method == 'GET':
        userID = request.GET["post_id"]
        # add user to organization
        org = Organization.objects.get(user=request.user)
        membr = Member.objects.get(id=userID)
        org.members.remove(membr)
        membr.organizations.remove(org)
        membr.save()
        org.save()

        return HttpResponse("Success!")
    return HttpResponse("An error has occurred...")

@login_required
def declineMember(request):
    
    if request.method == 'GET':
        userID = request.GET["post_id"]
        # add user to organization
        org = Organization.objects.get(user=request.user)
        membr = Member.objects.get(id=userID)
        o_req = Organization_Request.objects.get(from_user=membr, to_org=org)
        o_req.delete()
        return HttpResponse("Success!")
    return HttpResponse("An error has occurred...")

@login_required
def myMembers(request):
    org = Organization.objects.get(user=request.user)
    # get requesting users...
    
    requesting_users = []
    org_requests = Organization_Request.objects.filter(to_org=org)
    for reqs in org_requests:
        requesting_users.append(reqs.from_user)
    context = {
        "org": org,
        "members": org.members.all(),
        "requestingUsers": requesting_users,
    }
    return render(request, "organization-members.html", context)


# @login_required
def viewEvent(request, eventID):
    e = Event.objects.get(id=eventID)
    context = {
        "event": e,
        "edittable": False,
        "friends": None
    }
    if request.user.is_authenticated:
        # if private event, check that user
        event_organizer = None
        try:
            event_organizer = Member.objects.get(user=e.organizer)
        except:
            event_organizer = Organization.objects.get(user=e.organizer)
        
        if isinstance(event_organizer, Organization):
            # if it's an organization, check that member is part of the organization
            try:
                membr = Member.objects.get(user=request.user)
                
                t_friends = []
                e_temp = e.interested_members.all()
                for x in membr.friends.all():
                    if x in e_temp:
                        t_friends.append(x)
                # print(t_friends)
                context['friends'] = t_friends
                if event_organizer in membr.organizations.all() or e.public_event:
                    return render(request, "event-view.html", context)
            except:
                org = Organization.objects.get(user=request.user)
                if event_organizer == org:
                    context["edittable"] = True
                    return render(request, "event-view.html", context)
        else:
            # the organizer is a user
            try:
                membr = Member.objects.get(user=request.user)
                context['friends'] = membr.friends.all()
                if event_organizer == membr:
                    context["edittable"] = True
                    return render(request, "event-view.html", context)    
                if event_organizer in membr.friends.all():
                    return render(request, "event-view.html", context)
            except:
                pass

    if not request.user.is_authenticated and e.public_event:
        # let all users see if public event
        return render(request, "event-view.html", context)
    
    if not request.user.is_authenticated and not e.public_event:
        return redirect("/login")
    

    return HttpResponseNotFound("Permission Denied") # render(request, "success.html")

@login_required
def updateDB(request):
    if request.user.is_superuser:
        current_datetime = datetime.datetime.now()
        for e in Event.objects.all():
            if e.end_time < current_datetime and not e.organizer.is_superuser:
                # don't delete any admin events...
                e.delete()
        return render(request, "success.html")

    return HttpResponseNotFound("Permission Denied") 


@login_required
def deleteEvent(request, eventID):
    e = Event.objects.get(id=eventID)
    if request.user != e.organizer:
        return HttpResponseNotFound("Permission Denied") 
    e.delete()
    return render(request, "success.html")

@login_required
def removeFriend(request):
    if request.method == 'GET':
        memberID = request.GET["post_id"]
        # remove friendship
        membr = Member.objects.get(id=memberID)
        mem_usr = Member.objects.get(user=request.user)
        membr.friends.remove(mem_usr)
        mem_usr.friends.remove(membr)
        membr.save()
        mem_usr.save()
        return HttpResponse("Success! Friend removed...")
        # otherwise, organization is private and must accept
    else:
        return HttpResponse("Request method is not a GET")

@login_required
def userView(request, userID):
    membr_detail = Member.objects.get(user=User.objects.get(id=userID))

    friend_requests = Friend_Request.objects.filter(from_user=Member.objects.get(user=request.user))
    members_sent = [temp.to_user for temp in friend_requests]
    
    invites = Friend_Request.objects.filter(to_user=Member.objects.get(user=request.user))
    invite_members = [temp.from_user for temp in invites]
    
    context = {
        "member": membr_detail,
        "all_users": Member.objects.all(),
        "members_sent": set(members_sent),
        "invites": set(invite_members),
        "friends": Member.objects.get(user=request.user).friends.all(),
    }

    return render(request, "user-view.html", context)

@login_required
def editEvent(request, eventID):
    organizer = request.user
    org_check = False
    try:
        # if org, let org decide
        org = Organization.objects.get(user=request.user)
        org_check = True
    except:
        # else block
        org_check = False

    context = {
        "posted": False,

    }
    e = Event.objects.get(id=eventID)
    
    context["event"] = e
    if request.user != e.organizer:
        return HttpResponseNotFound("Permission Denied") 
    if request.method == "POST":
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            e.event_name =  form.cleaned_data["event_name"]
            e.description =  form.cleaned_data["description"]
            e.address =  form.cleaned_data["address"]
            e.address_details =  form.cleaned_data["address_details"]
            e.public_event = form.cleaned_data["public_event"]
            e.category = form.cleaned_data["category"]
            if org_check is False:
                e.public_event = False
            e.organizer = organizer
            # e.event_date = form.cleaned_data["event_date"]
            e.start_time = form.cleaned_data["start_time"]
            e.end_time = form.cleaned_data["end_time"]
            e.event_image = form.cleaned_data["event_image"]
            if e.address.latitude is None:
                return HttpResponse("Invalid Address...")
            
            e.RSVP_link = form.cleaned_data["RSVP_link"]
            e.save()
            context["posted"] = True
            return render(request, "success.html", context)
    else:
        form = EventCreation(
            initial={"event_name": e.event_name,
                     "description": e.description,
                     "address": e.address,
                     "address_details": e.address_details,
                     "public_event": e.public_event,
                    #  "event_date": e.description,
                     "start_time": e.start_time,
                     "end_time": e.end_time,
                     "event_image": e.event_image}
        )
    form.fields["public_event"].disabled = not org_check
    context["form"] = form
    return render(request, 'event-edit.html', context)


@login_required
def createEvent(request):
    organizer = request.user
    org_check = False
    try:
        # if org, let org decide
        org = Organization.objects.get(user=request.user)
        org_check = True
    except:
        # else block
        org_check = False
        
    context = {
        "posted": False,
        "key": settings.GOOGLE_API_KEY
    }
    if request.method == "POST":
        form = EventCreation(request.POST, request.FILES)
        if form.is_valid():
            e = Event()
            e.event_name =  form.cleaned_data["event_name"]
            e.description =  form.cleaned_data["description"]
            e.address =  form.cleaned_data["address"]
            e.category = form.cleaned_data["category"]
            e.address_details =  form.cleaned_data["address_details"]
            e.public_event = form.cleaned_data["public_event"]
            if org_check is False:
                e.public_event = False
            e.organizer = organizer
            # e.event_date = form.cleaned_data["event_date"]
            e.start_time = form.cleaned_data["start_time"]
            e.end_time = form.cleaned_data["end_time"]
            e.event_image = form.cleaned_data["event_image"]
            e.RSVP_link = form.cleaned_data["RSVP_link"]
            
            if e.address.latitude is None:
                return HttpResponse("Invalid Address...")
            
            e.save()
            context["posted"] = True
            return render(request, "success.html", context)
    else:
        form = EventCreation()

    form.fields["public_event"].disabled = not org_check
    context["form"] = form
    return render(request, 'event-creation.html', context)


# organization view of their events
@login_required
def my_events(request):
    org = Organization.objects.get(user=request.user)
    context = {
        "org": org,
        "events": Event.objects.filter(organizer=request.user)
    }
    return render(request, 'organization-events.html', context)
    
def organization_details(request):
    org = Organization.objects.get(user=request.user)
    context = {
        "org": org,
        "all_members": org.members.all(),
        "submitted": False,
    }
    if request.method == "POST":
        form = OrganizationProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # if existing, delete old profile picture
            if form.cleaned_data["image_upload"] != "":
                print("new picture")
                org.org_image = form.cleaned_data["image_upload"]
            org.name = form.cleaned_data["name"]
            org.description = form.cleaned_data["description"]
            org.public_org = form.cleaned_data["public_org"]
            org.save()
            context['submitted'] = True
    else:
        form = OrganizationProfileForm(initial={"name": org.name,
                                                "description": org.description,
                                                "public_org": org.public_org})
    
    context["form"] = form

    return render(request, 'organization-details.html', context)

from django.db.models import Count

def home(request):
    if not request.user.is_authenticated:
        return redirect("/login")
        # return render(request, 'home.html')
    
    request_user = None
    try:
        request_user = Member.objects.get(user=request.user)
    except:
        request_user = Organization.objects.get(user=request.user)


    current_datetime = datetime.datetime.now()
    cutoff_datetime = current_datetime + datetime.timedelta(days=TIME_DELTA)

    RECOMMENDED_COUNT = 10
    # if member, get all bookmarked events and relevant information
    bookmarked_events = []
    
    if isinstance(request_user, Member):
        for e in Event.objects.all():
            if request_user in e.interested_members.all() and current_datetime <= e.end_time and cutoff_datetime >= e.end_time:
                bookmarked_events.append(e)
    
    bookmarked_events.sort(key=lambda event: (event.start_time, event.getIMCount()), reverse=False)

    bookmarked_event_ids = [event.id for event in bookmarked_events]
    # temp_re = Event.objects.annotate(num_interest=Count('interested_members')).exclude(pk__in=bookmarked_event_ids).order_by('-num_interest')
    # recommended_events = temp_re[:min(len(temp_re), RECOMMENDED_COUNT)]
    blah = []
    e_count = 0
    for r in Event.objects.annotate(num_interest=Count('interested_members')).exclude(pk__in=bookmarked_event_ids).order_by('-num_interest'):
        if e_count == RECOMMENDED_COUNT:
            break

        if current_datetime <= r.end_time and cutoff_datetime >= r.end_time:
            e_count = e_count + 1
            blah.append(r)
    
    my_events = Event.objects.filter(organizer=request.user)
    current_datetime = datetime.datetime.now()
    cutoff_datetime = current_datetime + datetime.timedelta(days=TIME_DELTA)
    # all events
    future_events = []
    for i in my_events:
            if current_datetime <= i.end_time and cutoff_datetime >= i.end_time:
                future_events.append(i)

    context = {
        "bookmarked_events": bookmarked_events,
        "recommended_events": blah,
        "future_events": future_events,
        "is_member": isinstance(request_user, Member)
    }
    return render(request, "dashboard.html", context)


@login_required
def interest_form(request):

    # if they are a new user, create a feedback form... -- otherwise, redirect to main-page
    membr = None
    try:
        membr = Member.objects.get(user=request.user)
    except:
        pass

    if isinstance(membr, Member):
        if membr.new_user:
            if request.method == "POST":
                form = InterestForm(request.POST)
                if form.is_valid():
                    selected_choices = form.cleaned_data['interests']
                    whfrom = form.cleaned_data['where_from']
                    mbinfo = MemberInfo()
                    mbinfo.member = membr
                    mbinfo.member_interest = selected_choices
                    mbinfo.where_from = whfrom
                    mbinfo.save()
                    membr.new_user = False
                    return redirect("")
            else:
                form = InterestForm()
            return render(request, "interestform.html", {"form": form})
    return redirect("")


def error_404(request, exception):
    return render(request, "404.html", status=404)

@login_required
def feedback(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            fbO = FeedBack()
            fbO.feedback_info = form.cleaned_data["feedback_info"]
            fbO.user_feedback = request.user
            fbO.datetime_feedback = datetime.datetime.now()
            fbO.save()
            return render(request, "success.html")
    else:
        form = FeedBackForm()
    
    return render(request, "feedback.html", {'form': form})



@login_required
def organization_view(request, orgName):
    org = Organization.objects.get(name=orgName)
    membr = Member.objects.get(user=request.user)
    context = {
        "org": org,
        "joined": False,
        "requested_join": False
    }
    try:
        requested_join = Organization_Request.objects.get(from_user=membr, to_org=org)
        context['requested_join'] = True
    except:
        pass
        
    if membr in org.members.all():
        context['joined'] = True
    
    return render(request, "organization_view.html", context)

@login_required
def joinOrg(request):
    if request.method == 'GET':
        
        membr = Member.objects.get(user=request.user)
        org_id = request.GET['post_id']
        org = Organization.objects.get(id=org_id)
        # if organization is public, just join automatically
        if org.public_org:
            org.members.add(membr)
            membr.organizations.add(org)
            org.save()
            membr.save()
            return HttpResponse("Success! Organization Joined...")
        # otherwise, organization is private and must accept
        else:
            # create request
            m = Organization_Request(from_user=membr, to_org=org)
            m.save()
            return HttpResponse("Success! Organization invite pending...")
    else:
        return HttpResponse("Request method is not a GET")

@login_required
def leaveOrg(request):
    if request.method == 'GET':
        membr = Member.objects.get(user=request.user)
        org_id = request.GET['post_id']
        org = Organization.objects.get(id=org_id)
        org.members.remove(membr)
        membr.organizations.remove(org)
        return HttpResponse("Success. Organization left.")
        # otherwise, organization is private and must accept
    else:
        return HttpResponse("Request method is not a GET")

def organization_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data["username"]
            psword = form.cleaned_data["password"]
            user = authenticate(request, username=usrname, password=psword)
            if user is not None:
                login(request, user)
                return redirect("/map")
    else:
        form = LoginForm()
    
    return render(request, "organization-login.html", {'form': form})

@login_required
def organization_profile(request):
    org = Organization.objects.get(user=request.user)


    my_events = Event.objects.filter(organizer=request.user)
    current_datetime = datetime.datetime.now()
    cutoff_datetime = current_datetime + datetime.timedelta(days=TIME_DELTA)
    # all events
    future_events = []
    past_events = []
    for i in my_events:
            if current_datetime <= i.end_time and cutoff_datetime >= i.end_time:
                future_events.append(i)
            else:
                past_events.append(i)

    context = {
        "future_events": future_events,
        "past_events": past_events,
        "organization": org
    }
    return render(request, "organization-profile.html", context)

@login_required
def profile(request):
    try:
        membr = Member.objects.get(user=request.user)
    except:
        return organization_profile(request)

    all_friends = membr.friends.all()

    friend_requests = Friend_Request.objects.filter(to_user=membr)

    context = {
        'submitted': False,
        'member': membr,
        "friends": all_friends,
        "num_friends": len(all_friends),
        "friend_requests": friend_requests
    }


    
    # if request.method == "POST":
    #     form = ProfileForm(request.POST, request.FILES)
    #     # form = MyModelForm(request.POST, request.FILES)
        
    #     context['form'] = form
    #     if form.is_valid():
    #         # if existing, delete old profile picture
    #         membr.profile_pic = form.cleaned_data["image_upload"]
    #         membr.save()
    #         context['submitted'] = True
    # else:
    #     form = ProfileForm()

    # context['form'] = form
    return render(request, "social.html", context)

@login_required
def addFriendRequest(request):
    if request.method == 'GET':        
        member_id = request.GET['post_id']
        req_member = Member.objects.get(user=User.objects.get(id=member_id))
        try:
            usr_membr = Member.objects.get(user=request.user)
            frq_lookup = Friend_Request.objects.filter(from_user=req_member, to_user=usr_membr)
            if frq_lookup:
                usr_membr.friends.add(req_member)
                req_member.friends.add(usr_membr)
                frq_lookup.delete()
                return HttpResponse("Accepted")
        except:
            pass
        # friend request does not exist already -- create one
        m = Friend_Request(from_user=Member.objects.get(user=request.user), to_user=req_member) 
        m.save()  # saving it to store in database
        return HttpResponse("Sent") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")
    
@login_required
def removeFriendRequest(request):
    if request.method == 'GET':        
        member_id = request.GET['post_id']
        fr_member = Member.objects.get(user=request.user)
        # print(fr_member)
        t_member = Member.objects.get(user=User.objects.get(id=member_id)) #getting the liked posts
        # print(t_member)
        m = Friend_Request.objects.get(from_user=t_member, to_user=fr_member)
        m.delete()
        return HttpResponse("Success!") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

@login_required
def friends(request):
    # friend_requests = Friend_Request.objects.filter(from_user=Member.objects.get(user=request.user))
    # members_sent = [temp.to_user for temp in friend_requests]
    
    # invites = Friend_Request.objects.filter(to_user=Member.objects.get(user=request.user))
    # invite_members = [temp.from_user for temp in invites]

    membr = None
    try:
        membr = Member.objects.get(user=request.user)
    except:
        pass

    if isinstance(membr, Member):
        incoming_freq = None
        outgoing_freq = None
        try:
            incoming_freq = [t.from_user for t in Friend_Request.objects.filter(to_user=membr)]
        except:
            pass
        
        try:
            outgoing_freq = [t.to_user for t in Friend_Request.objects.filter(from_user=membr)]
        except:
            pass

        # print(incoming_freq)
        # print(outgoing_freq)
        context = {
            "all_users": Member.objects.all(),
            "friends": membr.friends.all(),
            "incoming_freq": incoming_freq,
            "outgoing_freq": outgoing_freq
        }
        return render(request, "friends.html", context)
    return HttpResponseNotFound("Permission Denied") 

@login_required
def organizations(request):
    membr = Member.objects.get(user=request.user)
    
    org_requests = Organization_Request.objects.filter(from_user=membr)
    requested_orgs = [temp.to_org for temp in org_requests]
    context = {
        "allorgs": Organization.objects.all(),
        "joined_orgs": membr.organizations.all(),
        "requested_orgs": requested_orgs
    }
    return render(request, "organizations.html", context)

def login_view(request):
    return render(request, 'login.html')

# TODO: Speed up queries https://www.softkraft.co/django-speed-up-queries/

# @login_required
def MapView(request):
    key = settings.GOOGLE_API_KEY
    membr = None

    
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        try:
            membr = Member.objects.get(user=request.user)
        except:
            membr = Organization.objects.get(user=request.user)
    
    isMember = isinstance(membr, Member)
    
    # get all public_events
    public_events = list(Event.objects.filter(public_event=True).distinct())


    # list of all private events from organizations that membr is part of
    private_events_orgs = []
    if isMember:
        for org in membr.organizations.only("user"):
            private_events = Event.objects.filter(organizer=org.user, public_event=False)
            for i in private_events:
                private_events_orgs.append(i)

    
    # list of all private events from friends
    friends_events = []
    # orgs dont' have friends :(
    if isMember:
        for e in membr.friends.only("user"):
            private_friend_events = Event.objects.filter(organizer=e.user, 
                                                         public_event=False)
            for i in private_friend_events:
                friends_events.append(i)

    # get your events
    my_events = []
    if is_authenticated:
        for e in list(Event.objects.filter(organizer=request.user)):
            my_events.append(e)

    all_events = [public_events, private_events_orgs, friends_events, my_events]
    locations = []
    

    # all events
    current_datetime = datetime.datetime.now()
    cutoff_datetime = current_datetime + datetime.timedelta(days=TIME_DELTA)
    ae = []
    for i in all_events:
        for j in i:
            if current_datetime <= j.end_time and cutoff_datetime >= j.end_time:
                ae.append(j)

    ae = set(ae)
    ae = list(ae)
    # sort by most popular...
    ae.sort(key=lambda event: (event.start_time, event.getIMCount()), reverse=False)

    for l in ae:
        # for l in a:
            scale_factor = 10**(-1)
            rand_lat_float = random.uniform(-0.001, 0.001) * scale_factor
            rand_lng_float = random.uniform(-0.001, 0.001) * scale_factor
            add_details = ""
            if l.address_details is not None:
                add_details = l.address_details
            if l.address.latitude is None or l.address.longitude is None:
                ae.remove(l)
                continue
            data = {
                "id": l.id,
                "lat": float(l.address.latitude + rand_lat_float),
                "lng": float(l.address.longitude + rand_lng_float),
                "name": l.event_name,
                # "description": l.description,
                "address": l.address.raw,
                "address_details": add_details,
                # "public_event": l.public_event,
                "organizer": l.getOrganizerName(),
                "start_time": str(l.start_time),
                "end_time": str(l.end_time),
                "category": l.category,
                "temp_icon": l.getEventIcon(),
                "isToday": str(l.isToday()),
            }
            locations.append(data)
    
    fd = [t[0] for t in EVENT_CATEGORIES]
    sd = [(t[0], t[1]) for t in EVENT_CATEGORIES]

    context = {
        "key": key,
        "locations": locations,
        "all_events": ae,
        "isMember": isMember,
        "member": membr,
        "event_categories": EVENT_CATEGORIES,
        "event_values": fd,
        "sd": sd,
        "current_date": current_datetime
    }

    return render(request, "map.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = Member.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )

    if created:
        return HttpResponse("Friend request sent")
    else:
        return HttpResponse("Friend request was already sent")

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friend.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse("friend request accepted")
    else:
        return HttpResponse("friend request not accepted")

