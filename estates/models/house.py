from django.conf import settings
from django.db import models

from .estate import Estate


class House(models.Model):
    class PropertyType(models.TextChoices):
        HOUSE = "HOUSE", "House"
        DUPLEX = "DUPLEX", "Duplex"
        APARTMENT = "APARTMENT", "Apartment"
        FLAT = "FLAT", "Flat"
        OTHER = "OTHER", "Other"

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name="houses",
    )

    property_number = models.CharField(
        max_length=50,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.HOUSE,
    )

    is_occupied = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estate", "property_number"],
                name="unique_property_number_per_estate",
            )
        ]

    def __str__(self):
        return f"{self.estate.name} - {self.property_number}"


class HouseResident(models.Model):
    class RelationshipType(models.TextChoices):
        OWNER = "OWNER", "Owner"
        TENANT = "TENANT", "Tenant"
        FAMILY = "FAMILY", "Family Member"
        OTHER = "OTHER", "Other"

    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="residents",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="houses",
    )

    relationship_type = models.CharField(
        max_length=20,
        choices=RelationshipType.choices,
        default=RelationshipType.TENANT,
    )

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["house", "user"],
                name="unique_house_resident",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.house}"



class HouseholdMember(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="household_members",
    )

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    relationship = models.CharField(
        max_length=50,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.house}"