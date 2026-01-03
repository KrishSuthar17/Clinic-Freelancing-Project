# clinic_app/utils/audit.py

from clinic_app.models import AuditLog

def log_action(request, action, phone=None, meta=None):
    AuditLog.objects.create(
        action=action,
        phone=phone,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        meta=meta or {}
    )


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0]
    return request.META.get('REMOTE_ADDR')
