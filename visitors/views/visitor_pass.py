from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from estates.models import (
    EstateMembership,
    Gate,
    HouseResident,
)
from visitors.serializers.visitor_pass import VisitorPassSerializer
from visitors.services.pass_verification import verify_visitor_pass
from visitors.models import VisitorPass


class VisitorPassCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_membership(self, request):
        return (
            EstateMembership.objects
            .filter(
                user=request.user,
                is_active=True,
                estate__is_active=True,
            )
            .select_related("estate")
            .first()
        )

    def get(self, request):
        visitor_passes = (
            VisitorPass.objects
            .filter(
                host=request.user,
                estate__is_active=True,
            )
            .select_related(
                "visitor",
                "estate",
                "house",
                "gate",
            )
            .order_by("-created_at")
        )

        serializer = VisitorPassSerializer(
            visitor_passes,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        membership = self.get_membership(request)

        if not membership:
            return Response(
                {
                    "detail": (
                        "You are not an active member of an estate."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        house_resident = (
            HouseResident.objects
            .filter(
                user=request.user,
                house__estate=membership.estate,
                house__is_active=True,
            )
            .select_related("house")
            .first()
        )

        if not house_resident:
            return Response(
                {
                    "detail": (
                        "You are not assigned to an active house."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = VisitorPassSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        visitor_pass = serializer.save(
            estate=membership.estate,
            house=house_resident.house,
            host=request.user,
        )

        return Response(
            VisitorPassSerializer(visitor_pass).data,
            status=status.HTTP_201_CREATED,
        )

class VisitorPassListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visitor_passes = (
            VisitorPass.objects
            .filter(
                host=request.user,
                estate__is_active=True,
            )
            .select_related(
                "visitor",
                "estate",
                "house",
                "gate",
            )
            .order_by("-created_at")
        )

        serializer = VisitorPassSerializer(
            visitor_passes,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class ActivateVisitorPassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pass_id):
        membership = (
            EstateMembership.objects
            .filter(
                user=request.user,
                is_active=True,
                estate__is_active=True,
            )
            .select_related("estate")
            .first()
        )

        if not membership:
            return Response(
                {
                    "detail": "You are not an active member of an estate."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        visitor_pass = (
            VisitorPass.objects
            .select_related("estate")
            .filter(
                id=pass_id,
                estate=membership.estate,
                host=request.user,
            )
            .first()
        )

        if not visitor_pass:
            return Response(
                {
                    "detail": "Visitor pass not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if visitor_pass.status != VisitorPass.Status.PENDING:
            return Response(
                {
                    "detail": "Only pending visitor passes can be activated."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        visitor_pass.status = VisitorPass.Status.ACTIVE
        visitor_pass.save(
            update_fields=["status", "updated_at"]
        )

        return Response(
            {
                "detail": "Visitor pass activated successfully.",
                "pass": VisitorPassSerializer(visitor_pass).data,
            },
            status=status.HTTP_200_OK,
        )


class VerifyVisitorPassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_code = request.data.get("access_code")
        gate_id = request.data.get("gate_id")

        if not access_code:
            return Response(
                {"detail": "Access code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not gate_id:
            return Response(
                {"detail": "Gate is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership = (
            EstateMembership.objects
            .select_related("estate")
            .filter(
                user=request.user,
                is_active=True,
                estate__is_active=True,
            )
            .first()
        )

        if not membership:
            return Response(
                {
                    "detail": (
                        "You are not an active member of an estate."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        estate = membership.estate

        gate = (
            Gate.objects
            .filter(
                id=gate_id,
                estate=estate,
                is_active=True,
            )
            .first()
        )

        if not gate:
            return Response(
                {"detail": "Invalid or inactive gate."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = verify_visitor_pass(
            access_code=access_code,
            estate=estate,
            gate=gate,
            security_officer=request.user,
        )

        if not result["valid"]:
            return Response(
                {
                    "valid": False,
                    "reason": result["reason"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        visitor_pass = result["pass"]

        return Response(
            {
                "valid": True,
                "reason": result["reason"],
                "pass": {
                    "id": visitor_pass.id,
                    "access_code": visitor_pass.access_code,
                    "visitor": visitor_pass.visitor.full_name,
                    "house": visitor_pass.house.property_number,
                    "host": visitor_pass.host.get_full_name(),
                    "gate": (
                        visitor_pass.gate.name
                        if visitor_pass.gate
                        else None
                    ),
                    "visit_date": visitor_pass.visit_date,
                    "expected_arrival": visitor_pass.expected_arrival,
                    "expected_departure": visitor_pass.expected_departure,
                    "status": visitor_pass.get_status_display(),
                },
            },
            status=status.HTTP_200_OK,
        )