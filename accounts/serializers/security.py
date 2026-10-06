
from django.contrib.auth import get_user_model
from rest_framework import serializers

from estates.models import EstateMembership

User = get_user_model()


class SecurityOfficerCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def create(self, validated_data):
        estate = self.context["estate"]

        user = User.objects.create(
            username=validated_data["email"],
            role=User.Role.SECURITY,
            **validated_data,
        )

        user.set_unusable_password()
        user.save()

        EstateMembership.objects.create(
            user=user,
            estate=estate,
            role=EstateMembership.Role.SECURITY,
            is_active=True,
        )

        return user

