from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

from accounts.models import Invitation
from accounts.services.invitation import generate_invitation_code

from estates.models import EstateMembership
from accounts.serializers.resident import ResidentCreateSerializer

User = get_user_model()



class ResidentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        membership = (
            EstateMembership.objects
            .filter(
                user=request.user,
                role=EstateMembership.Role.ESTATE_ADMIN,
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
                        "Only an active Estate Admin "
                        "can create residents."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ResidentCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        house = serializer.validated_data["house"]

        if house.estate_id != membership.estate_id:
            return Response(
                {
                    "detail": (
                        "You can only assign residents "
                        "to houses in your estate."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user = serializer.save()

        invitation = Invitation.objects.create(
            user=user,
            estate=membership.estate,
            code=generate_invitation_code(),
            expires_at=timezone.now() + timedelta(days=7),
        )

        return Response(
            {
                "detail": "Resident created successfully.",
                "resident": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "role": user.role,
                },
                "invitation": {
                    "code": invitation.code,
                    "expires_at": invitation.expires_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class ResidentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        membership = (
            EstateMembership.objects
            .filter(
                user=request.user,
                role=EstateMembership.Role.ESTATE_ADMIN,
                is_active=True,
                estate__is_active=True,
            )
            .select_related("estate")
            .first()
        )

        if not membership:
            return Response(
                {
                    "detail": "You are not an active estate admin."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        residents = (
            User.objects
            .filter(
                role=User.Role.RESIDENT,
                estate_memberships__estate=membership.estate,
                estate_memberships__is_active=True,
            )
            .distinct()
            .order_by("first_name", "last_name")
        )

        data = [
            {
                "id": resident.id,
                "first_name": resident.first_name,
                "last_name": resident.last_name,
                "email": resident.email,
                "phone_number": resident.phone_number,
                "role": resident.role,
            }
            for resident in residents
        ]

        return Response(data)

