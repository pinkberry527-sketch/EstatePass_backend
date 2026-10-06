from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from visitors.models import AccessLog


class SecurityDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()

        # Today's statistics
        logs_today = (
            AccessLog.objects
            .filter(created_at__date=today)
        )

        total_checks = logs_today.count()

        allowed = logs_today.filter(
            result=AccessLog.Result.ALLOWED
        ).count()

        denied = logs_today.filter(
            result=AccessLog.Result.DENIED
        ).count()

        # Recent access activity
        recent_logs = (
            AccessLog.objects
            .select_related(
                "visitor_pass",
                "security_officer",
            )
            .order_by("-created_at")[:10]
        )

        recent_activity = []

        for log in recent_logs:
            recent_activity.append({
                "id": log.id,
                "result": log.result,
                "reason": log.reason,
                "created_at": log.created_at,
                "visitor": (
                    str(log.visitor_pass.visitor)
                    if log.visitor_pass
                    else None
                ),
            })

        return Response({
            "total_checks": total_checks,
            "allowed": allowed,
            "denied": denied,
            "recent_activity": recent_activity,
        })