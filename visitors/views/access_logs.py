
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from visitors.models import AccessLog


class AccessLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AccessLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = (
            AccessLog.objects
            .select_related(
                "visitor_pass",
                "security_officer",
            )
            .order_by("-created_at")
        )

        paginator = AccessLogPagination()

        page = paginator.paginate_queryset(
            logs,
            request,
            view=self,
        )

        data = []

        for log in page:
            data.append({
                "id": log.id,
                "result": log.result,
                "reason": log.reason,
                "checked_in_at": log.checked_in_at,
                "checked_out_at": log.checked_out_at,
                "created_at": log.created_at,
                "visitor": (
                    str(log.visitor_pass.visitor)
                    if log.visitor_pass
                    else None
                ),

                "gate": (
                    str(log.gate)
                    if log.gate
                    else None
                ),
            })

        return paginator.get_paginated_response(data)

