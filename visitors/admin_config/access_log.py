from django.contrib import admin

from visitors.models import AccessLog


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):

    list_display = (
        "visitor_pass",
        "estate",
        "gate",
        "security_officer",
        "result",
        "created_at",
    )

    list_filter = (
        "result",
        "estate",
        "gate",
    )

    search_fields = (
        "visitor_pass__access_code",
        "visitor_pass__visitor__first_name",
        "visitor_pass__visitor__last_name",
        "security_officer__username",
    )

    readonly_fields = (
        "created_at",
    )