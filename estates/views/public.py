from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from estates.models import Estate


class PublicEstateListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        estates = (
            Estate.objects
            .filter(is_active=True)
            .order_by("name")
        )

        data = [
            {
                "id": estate.id,
                "name": estate.name,
            }
            for estate in estates
        ]

        return Response(data)