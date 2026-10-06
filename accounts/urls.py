from django.urls import path

from accounts.views.token import (
    CookieTokenRefreshView,
    LogoutView,
)

from accounts.views.auth import (
    EmailLoginView,
    CurrentUserView,
)

from accounts.views.invitation import (
    InvitationAcceptView,
    InvitationVerifyView,
)
from accounts.views.resident import ResidentCreateView, ResidentListView
from accounts.views.security import SecurityOfficerListView,   SecurityOfficerCreateView
from accounts.views.estate_admin import EstateAdminRegisterView


urlpatterns = [
    path(
        "login/",
        EmailLoginView.as_view(),
        name="login",
    ),

    path(
        "me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),

    path(
    "token/refresh/",
    CookieTokenRefreshView.as_view(),
    name="token-refresh",
    ),

    path(
    "invitations/verify/",
    InvitationVerifyView.as_view(),
    name="invitation-verify",
   ),

   path(
    "invitations/accept/",
    InvitationAcceptView.as_view(),
    name="invitation-accept",
    ),

    path( "logout/", LogoutView.as_view(), name="logout", ),

    path(
        "residents/",
        ResidentCreateView.as_view(),
        name="resident-create",
    ),

    path(
    "residents/list/",
    ResidentListView.as_view(),
    name="resident-list",
   ),

   path(
    "security-officers/list/",
    SecurityOfficerListView.as_view(),
    name="security-officer-list",
   ),

   path(
    "security-officers/",
    SecurityOfficerCreateView.as_view(),
    name="security-officer-create",
   ),

   path(
    "register/estate-admin/",
    EstateAdminRegisterView.as_view(),
    name="estate-admin-register",
   ),
]