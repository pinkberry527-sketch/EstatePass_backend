import secrets
import string

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from estates.models import Estate, EstateMembership, House, Gate
from .visitor import Visitor


class VisitorPass(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        USED = "USED", "Used"
        EXPIRED = "EXPIRED", "Expired"
        CANCELLED = "CANCELLED", "Cancelled"

    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name="passes",
    )

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name="visitor_passes",
    )

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="visitor_passes",
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visitor_passes",
    )

    gate = models.ForeignKey(
        Gate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visitor_passes",
    )

    access_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    visit_date = models.DateField()

    expected_arrival = models.TimeField()

    expected_departure = models.TimeField(
        null=True,
        blank=True,
    )

    purpose = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def clean(self):
        errors = {}

        if self.house and self.estate:
            if self.house.estate_id != self.estate_id:
                errors["house"] = (
                    "The selected property does not belong to this estate."
                )

        if self.gate and self.estate:
            if self.gate.estate_id != self.estate_id:
                errors["gate"] = (
                    "The selected gate does not belong to this estate."
                )

        if self.host and self.estate:
            membership_exists = EstateMembership.objects.filter(
                user=self.host,
                estate=self.estate,
                is_active=True,
            ).exists()

            if not membership_exists:
                errors["host"] = (
                    "The selected host is not an active member of this estate."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.access_code:
            self.access_code = self.generate_access_code()

        super().save(*args, **kwargs)

    @staticmethod
    def generate_access_code():
        characters = string.ascii_uppercase + string.digits

        return "".join(
            secrets.choice(characters)
            for _ in range(8)
        )


    def is_valid(self):
        now = timezone.localtime()

        if self.status != self.Status.ACTIVE:
            return False

        if self.visit_date != now.date():
            return False

        current_time = now.time()

        if current_time < self.expected_arrival:
            return False

        if (
            self.expected_departure
            and current_time > self.expected_departure
        ):
            return False

        return True

    def __str__(self):
        return f"{self.visitor} - {self.access_code}"

    