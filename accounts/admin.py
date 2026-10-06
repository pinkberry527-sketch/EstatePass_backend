from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )


    fieldsets = UserAdmin.fieldsets + (
        (
            "EstatePass Information",
            {
                "fields": (
                    "phone_number",
                    "role",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "EstatePass Information",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "role",
                )
            },
        ),
    )

    ordering = ("-date_joined",)






