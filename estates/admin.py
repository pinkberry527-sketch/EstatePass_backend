from django.contrib import admin
from .models import (Estate,EstateMembership,House,HouseResident,Gate,)

# Register your models here.

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "state",
        "country",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "country",
        "state",
    )
    search_fields =(
         "name",
        "city",
        "state",
        "email",
        "phone_number",
    )
    ordering =(
        "-created_at",
    )


@admin.register(EstateMembership)
class EstateMembershipoAdmin(admin.ModelAdmin):
    list_display =(
        "user",
        "estate",
        "role",
        "is_active",
        "created_at",
        )
    list_filter =(
        "role",
        "is_active",
        "estate",
        )
    search_fields = (
        "user__username",
        "user__email",
        "estate__name",
    )
    autocomplete_fields = (
        "user",
        "estate",
    )

    ordering = ("-created_at",)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "property_number",
        "estate",
        "property_type",
        "is_occupied",
        "is_active",
        "created_at",
    )

    list_filter = (
        "property_type",
        "is_occupied",
        "is_active",
        "estate",
    )

    search_fields = (
        "property_number",
        "address",
        "estate__name",
    )

    autocomplete_fields = (
        "estate",
    )

    ordering = ("estate", "property_number")



@admin.register(HouseResident)
class HouseResidentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "house",
        "relationship_type",
        "is_primary",
        "created_at",
    )

    list_filter = (
        "relationship_type",
        "is_primary",
        "house__estate",
    )
    search_fields = (
        "user__username",
        "user__email",
        "house__property_number",
        "house__estate__name",
    )

    autocomplete_fields = (
        "user",
        "house",
    )

    ordering = ("-created_at",)



@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "estate",
        "location",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "estate",
    )

    search_fields = (
        "name",
        "location",
        "estate__name",
    )

    autocomplete_fields = (
        "estate",
    )

    ordering = ("estate", "name")


        

