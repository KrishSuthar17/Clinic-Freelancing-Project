from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from clinic_app.models import Appointment, Notification

@receiver(pre_save, sender=Appointment)
def store_previous_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
    else:
        instance._previous_status = (
            Appointment.objects
            .filter(pk=instance.pk)
            .values_list("status", flat=True)
            .first()
        )

@receiver(post_save, sender=Appointment)
def appointment_status_changed(sender, instance, created, **kwargs):
    print("🔥 SIGNAL TRIGGERED")
    print("ID:", instance.id)
    print("OLD:", getattr(instance, "_previous_status", None))
    print("NEW:", instance.status)

    if created:
        return

    old = getattr(instance, "_previous_status", None)
    new = instance.status

    if old == new:
        print("⏭ No status change")
        return

    if new == "confirmed":
        Notification.objects.create(
            recipient_type="patient",
            recipient_id=instance.phone,
            title="✅ Appointment Confirmed",
            message="Your appointment has been confirmed."
        )
        print("✅ CONFIRM NOTIFICATION CREATED")

    elif new == "cancelled":
        Notification.objects.create(
            recipient_type="patient",
            recipient_id=instance.phone,
            title="❌ Appointment Cancelled",
            message="Your appointment has been cancelled."
        )
        print("❌ CANCEL NOTIFICATION CREATED")
