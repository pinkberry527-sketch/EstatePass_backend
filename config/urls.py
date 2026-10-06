from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/",
        include("visitors.urls"),
    ),

    path(
        "api/auth/",
        include("accounts.urls"),
    ),

  path(
    "api/estates/",
    include("estates.urls"),
),

   
]