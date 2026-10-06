from visitors.models import AccessLog, VisitorPass


def verify_visitor_pass(
    access_code,
    estate,
    gate=None,
    security_officer=None,
):
    try:
        visitor_pass = (
            VisitorPass.objects
            .select_related(
                "visitor",
                "house",
                "host",
                "gate",
            )
            .get(
                access_code=access_code,
                estate=estate,
            )
        )

    except VisitorPass.DoesNotExist:

        AccessLog.objects.create(
            visitor_pass=None,
            estate=estate,
            gate=gate,
            security_officer=security_officer,
            result=AccessLog.Result.DENIED,
            reason="Visitor pass not found.",
        )

        return {
            "valid": False,
            "reason": "Visitor pass not found.",
            "pass": None,
        }

    if not visitor_pass.is_valid():

        AccessLog.objects.create(
            visitor_pass=visitor_pass,
            estate=estate,
            gate=gate,
            security_officer=security_officer,
            result=AccessLog.Result.DENIED,
            reason="Visitor pass is not valid.",
        )

        return {
            "valid": False,
            "reason": "Visitor pass is not valid.",
            "pass": visitor_pass,
        }

    AccessLog.objects.create(
        visitor_pass=visitor_pass,
        estate=estate,
        gate=gate,
        security_officer=security_officer,
        result=AccessLog.Result.ALLOWED,
        reason="Visitor pass verified successfully.",
    )

    return {
        "valid": True,
        "reason": "Visitor pass verified successfully.",
        "pass": visitor_pass,
    }