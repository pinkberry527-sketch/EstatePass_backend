from rest_framework import serializers

from estates.models import HouseholdMember


class HouseholdMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdMember
        fields = [
            "id",
            "first_name",
            "last_name",
            "relationship",
            "phone_number",
        ]
        read_only_fields = ["id"]