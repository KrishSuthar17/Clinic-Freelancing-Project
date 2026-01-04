
from clinic_app.models import Device, Notification
from clinic_app.tasks import send_push_notification

from clinic_app.models import Device
from clinic_app.firebase import send_fcm_push

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

    devices = Device.objects.filter(
        user_type="patient",
        phone=appointment.phone,
        is_active=True
    )

    print("📲 DEVICES FOUND:", devices.count())

    for device in devices:
        send_fcm_push(device.fcm_token, title, message)




