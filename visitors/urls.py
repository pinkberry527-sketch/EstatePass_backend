from django.urls import path

from visitors.views.visitor_pass import VerifyVisitorPassView, VisitorPassCreateView,  ActivateVisitorPassView, VisitorPassListView
from visitors.views.dashboard import SecurityDashboardView
from visitors.views.access_logs import AccessLogListView
from visitors.views.gates import GateListView
from visitors.views.access_tracking import CheckInVisitorView, CheckOutVisitorView


urlpatterns = [

    path(
    "visitor-passes/",
    VisitorPassCreateView.as_view(),
    name="visitor-pass-create",
   ),
    path(
        "visitor-passes/verify/",
        VerifyVisitorPassView.as_view(),
        name="verify-visitor-pass",
    ),

    path(
    "security-dashboard/",
    SecurityDashboardView.as_view(),
    name="security-dashboard",
   ),

   path(
    "access-logs/",
    AccessLogListView.as_view(),
    name="access-logs",
   ),

   path(
    "gates/",
    GateListView.as_view(),
    name="gate-list",
    ),

    path(
    "access-logs/<int:log_id>/check-in/",
    CheckInVisitorView.as_view(),
    name="check-in-visitor",
   ),

   path(
    "access-logs/<int:log_id>/check-out/",
    CheckOutVisitorView.as_view(),
    name="check-out-visitor",
   ),

   path(
    "visitor-passes/<int:pass_id>/activate/",
    ActivateVisitorPassView.as_view(),
    name="activate-visitor-pass",
  ),


  path(
    "visitor-passes/",
    VisitorPassListView.as_view(),
    name="visitor-pass-list",
  ),
]