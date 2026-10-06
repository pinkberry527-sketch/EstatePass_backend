from django.urls import path

from estates.views.house import HouseListView, MyHouseView
from estates.views.household import HouseholdMemberListCreateView,HouseholdMemberDetailView
from estates.views.public import PublicEstateListView


urlpatterns = [
    path(
        "houses/",
        HouseListView.as_view(),
        name="house-list",
    ),

    path(
    "my-house/",
    MyHouseView.as_view(),
    name="my-house",
    ),

    path(
    "household-members/",
    HouseholdMemberListCreateView.as_view(),
    name="household-members",
   ),

   path(
    "household-members/<int:pk>/",
    HouseholdMemberDetailView.as_view(),
    name="household-member-detail",
   ),


    path(
        "public/",
        PublicEstateListView.as_view(),
        name="public-estate-list",
    ),
]