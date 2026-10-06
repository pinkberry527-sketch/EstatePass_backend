
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from estates.models import HouseholdMember, HouseResident
from estates.serializers.household import HouseholdMemberSerializer


class HouseholdMemberListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_house(self, request):
        house_resident = (
            HouseResident.objects
            .filter(
                user=request.user,
                house__is_active=True,
                house__estate__is_active=True,
            )
            .select_related("house")
            .first()
        )

        if not house_resident:
            return None

        return house_resident.house

    def get(self, request):
        house = self.get_house(request)

        if not house:
            return Response(
                {"detail": "You are not assigned to a house."},
                status=400,
            )

        members = HouseholdMember.objects.filter(
            house=house
        ).order_by("first_name")

        serializer = HouseholdMemberSerializer(
            members,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        house = self.get_house(request)

        if not house:
            return Response(
                {"detail": "You are not assigned to a house."},
                status=400,
            )

        serializer = HouseholdMemberSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(house=house)

            return Response(
                serializer.data,
                status=201,
            )

        return Response(
            serializer.errors,
            status=400,
        )




class HouseholdMemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_house(self, request):
        house_resident = (
            HouseResident.objects
            .filter(
                user=request.user,
                house__is_active=True,
                house__estate__is_active=True,
            )
            .select_related("house")
            .first()
        )

        if not house_resident:
            return None

        return house_resident.house

    def get_member(self, request, pk):
        house = self.get_house(request)

        if not house:
            return None, Response(
                {"detail": "You are not assigned to a house."},
                status=400,
            )

        try:
            member = HouseholdMember.objects.get(
                id=pk,
                house=house,
            )
        except HouseholdMember.DoesNotExist:
            return None, Response(
                {"detail": "Household member not found."},
                status=404,
            )

        return member, None

    def patch(self, request, pk):
        member, error_response = self.get_member(request, pk)

        if error_response:
            return error_response

        serializer = HouseholdMemberSerializer(
            member,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400,
        )

    def delete(self, request, pk):
        member, error_response = self.get_member(request, pk)

        if error_response:
            return error_response

        member.delete()

        return Response(status=204)


