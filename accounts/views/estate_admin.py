from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.estate_admin import (
    EstateAdminRegisterSerializer,
)


class EstateAdminRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = EstateAdminRegisterSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return Response(
            {
                "detail": "Estate Admin account created successfully.",
                "estate_admin": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )