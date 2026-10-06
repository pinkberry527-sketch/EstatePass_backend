from django.contrib import admin
from ..models import VisitorPass


@admin.register(VisitorPass)
class VisitorPassAdmin(admin.ModelAdmin):
    list_display = (
        "access_code",
        "visitor",
        "estate",
        "house",
        "host",
        "gate",
        "visit_date",
        "status",
    )

    list_filter = (
        "status",
        "estate",
        "visit_date",
    )

    search_fields = (
        "access_code",
        "visitor__first_name",
        "visitor__last_name",
        "visitor__phone_number",
    )

    readonly_fields = (
        "access_code",
        "created_at",
        "updated_at",
    )