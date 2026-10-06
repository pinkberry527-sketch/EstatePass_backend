from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from visitors.models import AccessLog
from visitors.services.access_tracking import check_in_visitor, check_out_visitor


class CheckInVisitorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, log_id):
        try:
            access_log = AccessLog.objects.get(
                id=log_id,
                estate__memberships__user=request.user,
                estate__memberships__is_active=True,
            )
        except AccessLog.DoesNotExist:
            return Response(
                {
                    "detail": "Access log not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        result = check_in_visitor(access_log)

        if not result["success"]:
            return Response(
                {
                    "success": False,
                    "reason": result["reason"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "reason": result["reason"],
                "checked_in_at": access_log.checked_in_at,
            },
            status=status.HTTP_200_OK,
        )


class CheckOutVisitorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, log_id):
        try:
            access_log = AccessLog.objects.get(
                id=log_id,
                estate__memberships__user=request.user,
                estate__memberships__is_active=True,
            )
        except AccessLog.DoesNotExist:
            return Response(
                {
                    "detail": "Access log not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        result = check_out_visitor(access_log)

        if not result["success"]:
            return Response(
                {
                    "success": False,
                    "reason": result["reason"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "reason": result["reason"],
                "checked_out_at": access_log.checked_out_at,
            },
            status=status.HTTP_200_OK,
        )