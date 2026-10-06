from django.db import models

from .estate import Estate


class Gate(models.Model):
    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name="gates",
    )

    name = models.CharField(
        max_length=100,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estate", "name"],
                name="unique_gate_name_per_estate",
            )
        ]

    def __str__(self):
        return f"{self.estate.name} - {self.name}"