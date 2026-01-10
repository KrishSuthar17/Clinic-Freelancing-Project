import logging
from clinic_app.models import Device, Notification
from clinic_app.tasks import send_push_notification

logger = logging.getLogger(__name__)


# -----------------------------
# DOCTOR: new booking
# -----------------------------
def notify_doctor_new_booking(appointment):
    devices = Device.objects.filter(
        user_type="doctor",
        is_active=True
    )

    if not devices.exists():
        logger.info("No doctor devices found")
        return

    for device in devices:
        send_push_notification.delay(
            device.fcm_token,
            "New Appointment",
            f"New appointment from {appointment.patient_name}"
        )


# -----------------------------
# PATIENT: confirmation
# -----------------------------
def notify_patient_confirmation(appointment):
    title = "✅ Appointment Confirmed"
    message = "Your appointment has been confirmed by the doctor."

    # 1️⃣ Save DB notification
    Notification.objects.create(
        recipient_type="patient",
        recipient_id=str(appointment.phone),
        title=title,
        message=message
    )

    # 2️⃣ Get devices
    devices = Device.objects.filter(
        user_type="patient",
        phone=appointment.phone,
        is_active=True
    )

    if not devices.exists():
        logger.info(f"No patient devices for {appointment.phone}")
        return

    # 3️⃣ Send async notifications
    for device in devices:
        send_push_notification.delay(
            device.fcm_token,
            title,
            message
        )


# -----------------------------
# PATIENT: cancellation
# -----------------------------
def notify_patient_cancellation(appointment):
    title = "❌ Appointment Cancelled"
    message = "Your appointment has been cancelled by the doctor."

    # 1️⃣ Save DB notification
    Notification.objects.create(
        recipient_type="patient",
        recipient_id=str(appointment.phone),
        title=title,
        message=message
    )

    # 2️⃣ Get devices
    devices = Device.objects.filter(
        user_type="patient",
        phone=appointment.phone,
        is_active=True
    )

    if not devices.exists():
        logger.info(f"No patient devices for {appointment.phone}")
        return

    # 3️⃣ Send async notifications
    for device in devices:
        send_push_notification.delay(
            device.fcm_token,
            title,
            message
        )
