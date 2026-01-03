from django.core.management.base import BaseCommand
from django.utils import timezone
from clinic_app.models import Appointment

ANONYMIZE_AFTER_YEARS = 3
DELETE_AFTER_YEARS = 4


class Command(BaseCommand):
    help = "Run data retention: anonymize & delete old appointment data"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        anonymize_before = now - timezone.timedelta(days=365 * ANONYMIZE_AFTER_YEARS)
        delete_before = now - timezone.timedelta(days=365 * DELETE_AFTER_YEARS)

        # 🔹 STEP 1: ANONYMIZE OLD DATA
        anonymized = Appointment.objects.filter(
            created_at__lt=anonymize_before,
            is_anonymized=False
        )

        count_anon = anonymized.count()

        for appt in anonymized:
            appt.patient_name = "ANONYMIZED"
            appt.phone = "0000000000"
            appt.is_anonymized = True
            appt.anonymized_at = now
            appt.save(update_fields=[
                "patient_name",
                "phone",
                "is_anonymized",
                "anonymized_at"
            ])

        # 🔹 STEP 2: DELETE VERY OLD DATA
        deleted, _ = Appointment.objects.filter(
            created_at__lt=delete_before,
            is_anonymized=True
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Retention complete → Anonymized: {count_anon}, Deleted: {deleted}"
        ))
