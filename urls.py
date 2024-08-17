from django.urls import re_path, path
from django.contrib import admin
from . import views
import django

# def custom_page_not_found(request):
#     return django.views.defaults.page_not_found(request, None)


# handler404 = views.error_404

urlpatterns = [
    re_path("map", views.MapView),
    path("newUserForm", views.interest_form),
    path("refreshDB", views.updateDB),
    path("feedback", views.feedback),
    path("register", views.registerOrg),
    path("organization-details", views.organization_details),
    path("saveevent", views.saveEvent),
    path("organization-events", views.my_events),
    path("organization-members", views.myMembers),
    path("acceptuser", views.addMember),
    path("declineuser", views.declineMember),
    path("removeuser", views.removeMember),
    path("create-event", views.createEvent),
    path("removefriend", views.removeFriend),
    path("edit-event/<int:eventID>", views.editEvent),
    path("delete-event/<int:eventID>", views.deleteEvent),
    path("events/<int:eventID>", views.viewEvent),
    path("users/<int:userID>", views.userView),
    re_path("organization-login", views.organization_login),
    path("joinorg", views.joinOrg),
    path("leaveorg", views.leaveOrg),
    re_path("logout", views.logout_view),
    re_path("login", views.login_view),
    path("profile", views.profile),
    path("organizations/<str:orgName>", views.organization_view),
    path("likepost", views.addFriendRequest),
    path("removepost", views.removeFriendRequest),
    re_path("profile/organizations", views.organizations),
    re_path("profile/add-friends", views.friends),
    re_path("dashboard", views.home),
    re_path("api-request", views.API),
    re_path("$", views.MapView),
]

