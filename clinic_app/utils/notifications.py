
from clinic_app.models import Device, Notification
from clinic_app.tasks import send_push_notification

from clinic_app.models import Device
from clinic_app.firebase import send_fcm_push
from firebase_admin import messaging

def notify_doctor_new_booking(appointment):
    devices = Device.objects.filter(
        user_type="doctor",
        is_active=True
    )

    for d in devices:
        send_fcm_push(
            d.fcm_token,
            "New Appointment",
            f"New appointment from {appointment.patient_name}"
        )



def notify_patient_confirmation(appointment):
    title = "✅ Appointment Confirmed"
    message = "Your appointment has been confirmed by the doctor."

    Notification.objects.create(
        recipient_type="patient",
        recipient_id=appointment.phone,  # phone-based identity
        title=title,
        message=message
    )

    patient_device = Device.objects.filter(
        user_type="patient",
        phone = appointment.phone,
        is_active=True
    )

    # print("📲 DEVICES FOUND:", patient_device.count())

    for device in patient_device:
        send_fcm_push(device.fcm_token, title, message)
        send_push_notification.delay(
            device.fcm_token,
            "Appointment Confirmed",
            "Your appointment is confirmed."
        )



def notify_patient_cancellation(appointment):
    # print("🔥 NOTIFY PATIENT CANCELLATION:", appointment.phone)

    # 1️⃣ Save notification in DB
    Notification.objects.create(
        recipient_type="patient",
        recipient_id=int(appointment.phone),
        title="Appointment Cancelled",
        message="Your appointment has been cancelled by the doctor."
    )

    # 2️⃣ Get patient devices
    devices = Device.objects.filter(
        user_type="patient",
        phone=appointment.phone,
        is_active=True
    )

    # print("🔥 DEVICES FOUND:", devices.count())

    # 3️⃣ Send push to EACH device
    for d in devices:
        messaging.send(
            messaging.Message(
                notification=messaging.Notification(
                    title="Appointment Cancelled",
                    body="Your appointment has been cancelled by the doctor."
                ),
                token=d.fcm_token,  # ✅ CORRECT
            )
        )
