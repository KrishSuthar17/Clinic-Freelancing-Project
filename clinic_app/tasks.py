from celery import shared_task
from firebase_admin import messaging
from clinic_app.models import Device
from clinic_app.firebase_admin_init import init_firebase
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_push_notification(self, token, title, message):
    try:
        # 🔥 THIS LINE FIXES EVERYTHING
        init_firebase()

        messaging.send(
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=token,
            )
        )

    except messaging.UnregisteredError:
        Device.objects.filter(fcm_token=token).update(is_active=False)
        logger.warning(f"FCM token unregistered, deactivated → {token}")

        # DO NOT retry — token is dead
        return
    except Exception as e:
        logger.error(f"FCM send failed → {token} | {e}")
        raise self.retry(exc=e, countdown=10)
