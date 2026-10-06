
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Invitation
from accounts.serializers.security import SecurityOfficerCreateSerializer
from accounts.services.invitation import generate_invitation_code

from estates.models import EstateMembership


User = get_user_model()


class SecurityOfficerCreateView(APIView):
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
                {"detail": "You are not an active estate admin."},
                status=403,
            )

        serializer = SecurityOfficerCreateSerializer(
            data=request.data,
            context={"estate": membership.estate},
        )

        serializer.is_valid(raise_exception=True)

        officer = serializer.save()

        invitation = Invitation.objects.create(
            user=officer,
            estate=membership.estate,
            code=generate_invitation_code(),
            expires_at=timezone.now() + timedelta(days=7),
        )

        return Response(
            {
                "message": "Security officer created successfully.",
                "officer": {
                    "id": officer.id,
                    "first_name": officer.first_name,
                    "last_name": officer.last_name,
                    "email": officer.email,
                    "phone_number": officer.phone_number,
                    "role": officer.role,
                },
                "invitation": {
                    "code": invitation.code,
                    "expires_at": invitation.expires_at,
                },
            },
            status=201,
        )


class SecurityOfficerListView(APIView):
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
                {"detail": "You are not an active estate admin."},
                status=403,
            )

        officers = (
            User.objects
            .filter(
                role=User.Role.SECURITY,
                estate_memberships__estate=membership.estate,
                estate_memberships__is_active=True,
            )
            .distinct()
            .order_by("first_name", "last_name")
        )

        data = [
            {
                "id": officer.id,
                "first_name": officer.first_name,
                "last_name": officer.last_name,
                "email": officer.email,
                "phone_number": officer.phone_number,
                "role": officer.role,
            }
            for officer in officers
        ]

        return Response(data)

