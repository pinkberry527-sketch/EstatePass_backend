from rest_framework import serializers

from visitors.models import Visitor, VisitorPass
from visitors.serializers.visitor import VisitorSerializer


class VisitorPassSerializer(serializers.ModelSerializer):
    visitor = VisitorSerializer()

    class Meta:
        model = VisitorPass
        fields = [
            "id",
            "visitor",
            "estate",
            "house",
            "host",
            "gate",
            "access_code",
            "visit_date",
            "expected_arrival",
            "expected_departure",
            "purpose",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "estate",
            "house",
            "host",
            "access_code",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        visitor_data = validated_data.pop("visitor")

        visitor = Visitor.objects.create(
            **visitor_data
        )

        visitor_pass = VisitorPass.objects.create(
            visitor=visitor,
            **validated_data
        )

        return visitor_pass