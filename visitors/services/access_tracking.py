from django.utils import timezone

from visitors.models import AccessLog


def check_in_visitor(access_log):
    if access_log.result != AccessLog.Result.ALLOWED:
        return {
            "success": False,
            "reason": "Only allowed visitors can be checked in.",
        }

    if access_log.checked_in_at:
        return {
            "success": False,
            "reason": "Visitor has already been checked in.",
        }

    access_log.checked_in_at = timezone.now()
    access_log.save(update_fields=["checked_in_at"])

    return {
        "success": True,
        "reason": "Visitor checked in successfully.",
        "access_log": access_log,
    }


def check_out_visitor(access_log):
    if not access_log.checked_in_at:
        return {
            "success": False,
            "reason": "Visitor has not been checked in.",
        }

    if access_log.checked_out_at:
        return {
            "success": False,
            "reason": "Visitor has already been checked out.",
        }

    access_log.checked_out_at = timezone.now()
    access_log.save(update_fields=["checked_out_at"])

    return {
        "success": True,
        "reason": "Visitor checked out successfully.",
        "access_log": access_log,
    }