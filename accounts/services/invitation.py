
import secrets

from accounts.models import Invitation


CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_invitation_code():
    while True:
        code = "EP-" + "".join(
            secrets.choice(CHARACTERS)
            for _ in range(6)
        )

        if not Invitation.objects.filter(code=code).exists():
            return code
