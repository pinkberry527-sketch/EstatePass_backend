from django.contrib.auth import get_user_model
from rest_framework import serializers

from estates.models import Estate, EstateMembership


User = get_user_model()


class EstateAdminRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )
    estate = serializers.PrimaryKeyRelatedField(
        queryset=Estate.objects.filter(is_active=True),
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def create(self, validated_data):
        estate = validated_data.pop("estate")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=validated_data["email"],
            password=password,
            role=User.Role.ESTATE_ADMIN,
            **validated_data,
        )

        EstateMembership.objects.create(
            user=user,
            estate=estate,
            role=EstateMembership.Role.ESTATE_ADMIN,
            is_active=True,
        )

        return user