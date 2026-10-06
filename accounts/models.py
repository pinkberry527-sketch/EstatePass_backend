from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        PLATFORM_ADMIN ="PLATFORM_ADMIN","Platform Admin"
        ESTATE_ADMIN = "ESTATE_ADMIN", "Estate Admin"
        RESIDENT ="RESIDENT","Resident"
        SECURITY = "SECURITY","Security Officer"

    email =models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,blank=True)
    role =models.CharField(max_length=30,choices=Role.choices, default=Role.RESIDENT,)

    def __str__(self):
        return self.get_full_name() or self.username
    


class Invitation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="invitation",
    )

    estate = models.ForeignKey(
        "estates.Estate",
        on_delete=models.CASCADE,
        related_name="invitations",
    )

    code = models.CharField(
        max_length=12,
        unique=True,
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False,
    )

    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.code


