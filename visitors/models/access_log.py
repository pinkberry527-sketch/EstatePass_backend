from django.db import models


class AccessLog(models.Model):

    class Result(models.TextChoices):
        ALLOWED = "ALLOWED", "Allowed"
        DENIED = "DENIED", "Denied"

    visitor_pass = models.ForeignKey(
        "visitors.VisitorPass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="access_logs",
    )

    estate = models.ForeignKey(
        "estates.Estate",
        on_delete=models.CASCADE,
        related_name="access_logs",
    )

    gate = models.ForeignKey(
        "estates.Gate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="access_logs",
    )

    security_officer = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="access_logs",
    )

    result = models.CharField(
        max_length=20,
        choices=Result.choices,
    )

    reason = models.TextField(
        blank=True,
    )

    checked_in_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    checked_out_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.visitor_pass} - "
            f"{self.result}"
        )