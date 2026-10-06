from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from estates.models import EstateMembership, House


class HouseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        membership = (
            EstateMembership.objects
            .filter(
                user=request.user,
                is_active=True,
                estate__is_active=True,
            )
            .select_related("estate")
            .first()
        )

        if not membership:
            return Response(
                {
                    "detail": (
                        "You are not an active member "
                        "of an estate."
                    )
                },
                status=403,
            )

        houses = (
            House.objects
            .filter(
                estate=membership.estate,
                is_active=True,
            )
            .order_by("property_number")
        )

        data = [
            {
                "id": house.id,
                "property_number": house.property_number,
                "address": house.address,
                "property_type": house.property_type,
                "is_occupied": house.is_occupied,
            }
            for house in houses
        ]

        return Response(data)


class MyHouseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        house_resident = (
            request.user.houses
            .select_related("house", "house__estate")
            .filter(
                house__is_active=True,
            )
            .first()
        )

        if not house_resident:
            return Response(
                {
                    "detail": "You are not associated with a house."
                },
                status=404,
            )

        house = house_resident.house

        return Response(
            {
                "id": house.id,
                "property_number": house.property_number,
                "address": house.address,
                "property_type": house.property_type,
                "is_occupied": house.is_occupied,
                "relationship_type": house_resident.relationship_type,
                "is_primary": house_resident.is_primary,
            }
        )