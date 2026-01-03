
from clinic_app.models import Device, Notification
from clinic_app.tasks import send_push_notification

def notify_doctor_new_booking(appointment):
    # 1. Save notification for admin
    Notification.objects.create(
        recipient_type="doctor",
        recipient_id=appointment.doctor.id,
        title="New Appointment",
        message=f"{appointment.patient_name} booked {appointment.date} at {appointment.time_slot}"
    )

    # 2. Send push to doctor devices
    devices = Device.objects.filter(
        user_type="doctor",
        user_id=appointment.doctor.id,
        is_active=True
    )

    for device in devices:
        send_push_notification.delay(
            device.fcm_token,
            "New Appointment",
            "You have a new appointment request."
        )



def notify_patient_confirmation(appointment):
    Notification.objects.create(
        recipient_type="patient",
        recipient_id=appointment.id,
        title="Appointment Confirmed",
        message="Your appointment has been confirmed."
    )

    devices = Device.objects.filter(
        user_type="patient",
        user_id=appointment.id,
        is_active=True
    )

    for device in devices:
        send_push_notification.delay(
            device.fcm_token,
            "Appointment Confirmed",
            "Your appointment is confirmed."
        )
