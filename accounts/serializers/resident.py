
from django.contrib.auth import get_user_model
from rest_framework import serializers

from estates.models import EstateMembership, House, HouseResident

User = get_user_model()


class ResidentCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
    )
    house = serializers.PrimaryKeyRelatedField(
        queryset=House.objects.filter(is_active=True)
    )
    relationship_type = serializers.ChoiceField(
        choices=HouseResident.RelationshipType.choices,
        default=HouseResident.RelationshipType.TENANT,
    )
    is_primary = serializers.BooleanField(default=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def create(self, validated_data):
        house = validated_data.pop("house")

        relationship_type = validated_data.pop(
            "relationship_type"
        )

        is_primary = validated_data.pop("is_primary")

        user = User.objects.create(
            username=validated_data["email"],
            role=User.Role.RESIDENT,
            **validated_data,
        )

        user.set_unusable_password()
        user.save()

        EstateMembership.objects.create(
            user=user,
            estate=house.estate,
            role=EstateMembership.Role.RESIDENT,
            is_active=True,
        )

        HouseResident.objects.create(
            user=user,
            house=house,
            relationship_type=relationship_type,
            is_primary=is_primary,
        )

        return user

