from django.utils.timezone import now, timedelta
from django.db import transaction
from clinic_app.models import RateLimit

MAX_REQUESTS = 5
WINDOW_SECONDS = 300  # 5 minutes

def is_rate_limited(phone, ip):
    with transaction.atomic():
        obj, _ = RateLimit.objects.select_for_update().get_or_create(
            phone=phone,
            ip_address=ip,
            defaults={"count": 0, "window_start": now()}
        )

        if now() - obj.window_start > timedelta(seconds=WINDOW_SECONDS):
            obj.count = 1
            obj.window_start = now()
            obj.save()
            return False

        obj.count += 1
        obj.save()

        # 🚨 CRITICAL LINE
        return obj.count > MAX_REQUESTS

