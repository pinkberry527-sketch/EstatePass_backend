from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from estates.models import EstateMembership, Gate


class GateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        membership = (
            EstateMembership.objects
            .select_related("estate")
            .filter(
                user=request.user,
                is_active=True,
                estate__is_active=True,
            )
            .first()
        )

        if not membership:
            return Response(
                {
                    "detail": "You are not an active member of an estate."
                },
                status=403,
            )

        gates = (
            Gate.objects
            .filter(
                estate=membership.estate,
                is_active=True,
            )
            .order_by("name")
        )

        return Response([
            {
                "id": gate.id,
                "name": gate.name,
            }
            for gate in gates
        ])