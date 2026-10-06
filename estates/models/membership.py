from django.conf import settings
from django.db import models

from .estate import Estate


class EstateMembership(models.Model):
    class Role(models.TextChoices):
        ESTATE_ADMIN = "ESTATE_ADMIN", "Estate Admin"
        RESIDENT = "RESIDENT", "Resident"
        SECURITY = "SECURITY", "Security Officer"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="estate_memberships",
    )

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "estate"],
                name="unique_user_estate",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.estate}"