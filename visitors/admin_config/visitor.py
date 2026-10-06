from django.contrib import admin
from ..models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone_number",
        "email",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "email",
    )