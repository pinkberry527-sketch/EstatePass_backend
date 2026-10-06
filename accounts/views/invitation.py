
from django.utils import timezone

from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Invitation


class InvitationVerifySerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=12
    )


class InvitationVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InvitationVerifySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        try:
            invitation = Invitation.objects.select_related(
                "user",
                "estate",
            ).get(code=code)
        except Invitation.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid invitation code."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.is_used:
            return Response(
                {
                    "detail": "This invitation has already been used."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.expires_at <= timezone.now():
            return Response(
                {
                    "detail": "This invitation has expired."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not invitation.user.is_active:
            return Response(
                {
                    "detail": "This account is inactive."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "valid": True,
                "user": {
                    "first_name": invitation.user.first_name,
                    "last_name": invitation.user.last_name,
                    "email": invitation.user.email,
                    "role": invitation.user.role,
                },
                "estate": {
                    "id": invitation.estate.id,
                    "name": invitation.estate.name,
                },
            },
            status=status.HTTP_200_OK,
        )



class InvitationAcceptSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=12
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": (
                        "Passwords do not match."
                    )
                }
            )

        return data


class InvitationAcceptView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InvitationAcceptSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        password = serializer.validated_data["password"]

        try:
            invitation = Invitation.objects.select_related(
                "user",
                "estate",
            ).get(code=code)
        except Invitation.DoesNotExist:
            return Response(
                {
                    "detail": "Invalid invitation code."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.is_used:
            return Response(
                {
                    "detail": (
                        "This invitation has already been used."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if invitation.expires_at <= timezone.now():
            return Response(
                {
                    "detail": "This invitation has expired."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not invitation.user.is_active:
            return Response(
                {
                    "detail": "This account is inactive."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = invitation.user

        user.set_password(password)
        user.save()

        invitation.is_used = True
        invitation.used_at = timezone.now()
        invitation.save(
            update_fields=[
                "is_used",
                "used_at",
            ]
        )

        return Response(
            {
                "detail": (
                    "Account activated successfully. "
                    "You can now log in."
                )
            },
            status=status.HTTP_200_OK,
        )
