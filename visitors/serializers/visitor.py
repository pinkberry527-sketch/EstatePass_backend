from rest_framework import serializers

from visitors.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "photo",
            "id_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]