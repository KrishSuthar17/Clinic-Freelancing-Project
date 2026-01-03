from celery import shared_task
from firebase_admin import messaging

@shared_task(bind=True, max_retries=3)
def send_push_notification(self, token, title, message):
    try:
        messaging.send(
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=token,
            )
        )
    except Exception as e:
        self.retry(exc=e, countdown=5)
