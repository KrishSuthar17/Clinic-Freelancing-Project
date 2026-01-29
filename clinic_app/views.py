from multiprocessing import context
import os
import uuid
from django.shortcuts import render
from httpcore import request

from clinic_app.models import ClinicInfo, Disease, Doctor, HomeopathyAbout, LiveSession, Appointment, Device
from .forms import testimonials_reviews_forms
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404
from .models import ClinicHoliday, DoctorLeave, Homeopathy_end_about_content, Homeopathy_start_about_content, faq, testimonials_reviews, gallery, blog, contact_gallary
from .utils.time_slots import TIME_SLOTS
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils.notifications import notify_doctor_new_booking,notify_patient_confirmation
from django.utils.timezone import now
from django.db import IntegrityError, transaction
from .models import Device, Notification
from .tasks import send_push_notification
from .constants import MAX_APPOINTMENTS_PER_DAY
from .utils.notifications import notify_doctor_new_booking
from .utils.audit import log_action,get_client_ip
from uuid import UUID
from .utils.rate_limit import is_rate_limited
import re
from django.utils.dateparse import parse_date, parse_time
from django.contrib.auth.decorators import login_required
from datetime import date as dt_date
from django.core.exceptions import ValidationError

# Create your views here.
from .models import ClinicSchedule
from datetime import datetime

@login_required
def doctor_page(reqest):
    context = {
        "GOOGLE_MAPS_API_KEY" : os.getenv("google_apiKey"),
        "authDomain" : os.getenv("authDomain"),
        "projectId" : os.getenv("projectId"),
        "messagingSenderId" : os.getenv("messagingSenderId"),
        "appId" : os.getenv("appId"),
    }
    return render(reqest, 'doctor/dashboard.html', context)

def home_page(request):
    context = {
        "doctor": Doctor.objects.filter(is_active=True).first(),
        "diseases": Disease.objects.filter(is_active=True),
        "videos": LiveSession.objects.filter(is_active=True),
        "clinic": ClinicInfo.objects.first(),
       
        
    }
    return render(request, "home.html", context)

def homeopathy_page(request):
    context = {
        "doctor": Doctor.objects.filter(is_active=True).first(),
        "diseases": Disease.objects.filter(is_active=True),
        "videos": LiveSession.objects.filter(is_active=True),
        "clinic": ClinicInfo.objects.first(),
        "about": HomeopathyAbout.objects.filter(is_active=True).first(),
        "homeopathy_about1": Homeopathy_start_about_content.objects.first(),
        "homeopathy_about2": Homeopathy_end_about_content.objects.first(),
    }
    return render(request, "homeopathy_page.html",context)

def online_consultation_page(request):
    context = {
        "doctor": Doctor.objects.filter(is_active=True).first(),
        "diseases": Disease.objects.filter(is_active=True),
    }
    return render(request, "online_consultation_page.html",context)

def testimonials_page(request):
    faqs = faq.objects.all()
    if request.method == "POST":
        form = testimonials_reviews_forms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('home')
        else:
            messages.error(request, "Review is not submitted!")
    else:
        form = testimonials_reviews_forms()

    return render(request, "testimonials_page.html", {"form": form, "faqs": faqs})

# views.py

def faq_page(request):
    faqs = faq.objects.all()
    return render(request, "faqs_page.html", {"faqs": faqs})


def gallery_videos_page(request):
    videos = gallery.objects.all()
    return render(request, "gallery_videos_page.html", {"videos": videos})

def blogs_page(request):
    doctor = {
        "name": "Dr. Ketul Soni",
        "image": "images/doctor-hero.jpg",
        "description": (
            "Dr. Ketul Soni is an experienced homeopathic physician known for his patient-centric approach. "
            "He specializes in chronic diseases, lifestyle disorders, and constitutional homeopathy. "
            "With years of clinical experience, Dr. Soni focuses on treating the root cause rather than "
            "just symptoms, ensuring long-term healing and improved quality of life."
        ),
    }
    blogs = blog.objects.all()

    return render(request, "blogs_page.html", {"doctor": doctor, "blogs": blogs})

def content(request):
    photos = contact_gallary.objects.all()
    return render(request, "content.html", {"photos": photos})


def disease_page(request, slug=None):
    diseases = Disease.objects.all()
    selected_disease = None

    if slug:
        selected_disease = get_object_or_404(Disease, slug=slug)

    return render(request, "components/Diseases_detail.html", {
    "diseases": diseases,
    "selected_disease": selected_disease,
    })


def blog_detail(request, slug):
    blog_obj = get_object_or_404(blog, slug=slug)
    return render(request, 'components/Blog_details.html', {'blog': blog_obj})



def book_appointment(request):

     # =========================
    # GET → SHOW FORM
    # =========================
    if request.method == "GET":
        context = {
            "doctors": Doctor.objects.filter(is_active=True),
            "slots": TIME_SLOTS,
            "GOOGLE_MAPS_API_KEY" : os.getenv("google_apiKey"),
            "authDomain" : os.getenv("authDomain"),
            "projectId" : os.getenv("projectId"),
            "messagingSenderId" : os.getenv("messagingSenderId"),
            "appId" : os.getenv("appId"),
        }
        return render(request, "Appoinment.html", context)


    # =========================
    # POST → PROCESS BOOKING
    # =========================

    phone = request.POST.get("phone")
    key = request.POST.get("idempotency_key")
    ip = get_client_ip(request)

    # ---- Parse & validate date/time FIRST ----
    date_str = request.POST.get("date")
    time_str = request.POST.get("time")

    date_obj = parse_date(date_str)
    time_obj = parse_time(time_str)

    if not isinstance(date_str, str) or not isinstance(time_str, str):
        return render(request, "error.html", {
        "error": "Invalid date or time selected."
    })


    date_obj = parse_date(date_str)
    time_obj = parse_time(time_str)

    if not date_obj or not time_obj:
        return render(request, "error.html", {
            "error": "Invalid date or time format."
        })
    

    doctor = get_object_or_404(
        Doctor,
        id=request.POST.get("doctor"),
        is_active=True
    )

    # ❌ SUNDAY BLOCK
    if date_obj.weekday() == 6:
        return render(request, "error.html", {
            "error": "Appointments are not available on Sundays."
        })
    
     # ❌ CLINIC HOLIDAY
    if ClinicHoliday.objects.filter(date=date_obj).exists():
        return render(request, "error.html", {
            "error": "Clinic is closed on this date."
        })
    
    # ❌ DOCTOR LEAVE
    if DoctorLeave.objects.filter(
        doctor=doctor,
        start_date__lte=date_obj,
        end_date__gte=date_obj
    ).exists():
        return render(request, "error.html", {
            "error": "Doctor is unavailable on this date."
        })

    if time_obj not in TIME_SLOTS:
        return render(request, "error.html", {
            "error": "Invalid time slot selected."
        })
    

    # ---- CLINIC SCHEDULE VALIDATION (NEW) ----
    schedule = ClinicSchedule.objects.first()

    if schedule:
        selected_date_str = date_obj.strftime("%Y-%m-%d")
        weekday = date_obj.weekday()  # Monday=0 ... Sunday=6

        day_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        # ✅ Special OPEN date → allow
        if selected_date_str in schedule.special_open_dates:
            pass

        # ❌ Special CLOSED date
        elif selected_date_str in schedule.special_closed_dates:
            return render(request, "error.html", {
                "error": "Clinic is closed on this date."
            })

        # ❌ Weekly OFF (Sunday etc.)
        else:
            for d in schedule.weekly_off_days:
                if weekday == day_map.get(d.lower()):
                    return render(request, "error.html", {
                        "error": "Clinic is closed on this day."
                    })




    # ---- 1️⃣ IDEMPOTENCY (first, always) ----
    raw_key = request.POST.get("idempotency_key")

    if not raw_key:                         # blank allowed
        key = uuid.uuid4()
    else:
        try:
            key = UUID(raw_key)
        except Exception:
            key = uuid.uuid4()  
            
    # ---- 2️⃣ RATE LIMIT (only after valid input) ----
    if is_rate_limited(phone, ip):
        log_action(request, "RATE_LIMIT_BLOCK", phone=phone)
        return render(request, "error.html", {
            "error": "Too many requests. Try again later."
        })

    log_action(request, "BOOK_ATTEMPT", phone=phone)

    # ---- 3️⃣ DAILY LIMIT + CREATE (ATOMIC) ----
    try:
        with transaction.atomic():
            today_count = Appointment.objects.select_for_update().filter(
                phone=phone,
                date=date_obj
            ).count()

            if today_count >= MAX_APPOINTMENTS_PER_DAY:
                return render(request, "error.html", {
                    "error": "Daily appointment limit reached (max 4 per day)."
                })

            appointment = Appointment.objects.create(
                patient_name=request.POST.get("name"),
                phone=phone,
                doctor_id=request.POST.get("doctor"),
                date=date_obj,       
                time_slot=time_obj,  
                idempotency_key=key,
            )

    except IntegrityError as e:
        msg = str(e).lower()

        if "idempotency" in msg:
            error = "Duplicate request detected. Please refresh and try again."
        elif "doctor" in msg or "time_slot" in msg:
            error = "This time slot is already booked."
        else:
            error = "Something went wrong. Please try again."

        return render(request, "error.html", {"error": error})


    # ---- 4️⃣ NOTIFY DOCTOR (AFTER COMMIT) ----
    notify_doctor_new_booking(appointment)
    context = {
        "appointment": appointment,
        "GOOGLE_MAPS_API_KEY" : os.getenv("google_apiKey"),
        "authDomain" : os.getenv("authDomain"),
        "projectId" : os.getenv("projectId"),
        "messagingSenderId" : os.getenv("messagingSenderId"),
        "appId" : os.getenv("appId"),
    }
    return render(request, "success.html", context)



def register_device(request):
    print("🔥 REGISTER DEVICE HIT")
    print("POST DATA:", request.POST)

    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    token = request.POST.get("token")
    user_type = request.POST.get("user_type")
    phone = request.POST.get("phone")

    if not token or not user_type:
        return JsonResponse({"error": "Missing token or user_type"}, status=400)

    # ==========================
    # 🔥 STEP 1: deactivate SAME token used elsewhere
    # (role switch / stale entry case)
    # ==========================
    Device.objects.filter(
        fcm_token=token,
        is_active=True
    ).update(is_active=False)

    # ==========================
    # PATIENT
    # ==========================
    if user_type == "patient":
        if not phone:
            return JsonResponse({"error": "Phone is required for patient"}, status=400)

        # 🔥 STEP 2: only ONE active device per phone
        Device.objects.filter(
            user_type="patient",
            phone=phone,
            is_active=True
        ).exclude(
            fcm_token=token
        ).update(is_active=False)

        device, _ = Device.objects.update_or_create(
            user_type="patient",
            phone=phone,
            fcm_token=token,
            defaults={
                "user": None,
                "is_active": True,
            }
        )

    # ==========================
    # DOCTOR
    # ==========================
    elif user_type == "doctor":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        # 🔥 STEP 2: only ONE active device per doctor
        Device.objects.filter(
            user_type="doctor",
            user=request.user,
            is_active=True
        ).exclude(
            fcm_token=token
        ).update(is_active=False)

        device, _ = Device.objects.update_or_create(
            user_type="doctor",
            user=request.user,
            fcm_token=token,
            defaults={
                "phone": None,
                "is_active": True,
            }
        )

    else:
        return JsonResponse({"error": "Invalid user_type"}, status=400)

    print("✅ DEVICE REGISTERED:", user_type, phone or request.user.id)

    return JsonResponse({
        "status": "registered",
        "device_id": device.id
    })






# appointment already saved safely here

# 1️⃣ Save admin notification
def confirm_appointment(appointment):
    appointment.status = "confirmed"
    appointment.save()

    Notification.objects.create(
        recipient_type="patient",
        recipient_id=int(appointment.phone), 
        title="Appointment Confirmed",
        message="Your appointment has been confirmed."
    )

    patient_device = Device.objects.filter(
        user_type="patient",
        phone = appointment.phone,
        is_active=True
    )


    for d in patient_device:
        send_push_notification.delay(
            d.fcm_token,
            "Appointment Confirmed",
            "Your appointment is confirmed."
        )




def patient_notifications(request):
    notifications = []
    phone = None
    error = None

    if request.method == "POST":
        phone = request.POST.get("phone")

        if not phone:
            error = "Phone number is required."
        elif not re.match(r"^[6-9]\d{9}$", phone):
            error = "Enter a valid 10-digit mobile number."
        else:
            notifications = (
                Notification.objects
                .filter(
                    recipient_type="patient",
                    recipient_id=int(phone)
                )
                .order_by("-created_at")[:4]
            )

            if not notifications:
                error = "No notifications found for this number."
    context = {
        "notifications": notifications,
        "phone": phone,
        "error": error,
        "GOOGLE_MAPS_API_KEY" : os.getenv("google_apiKey"),
        "authDomain" : os.getenv("authDomain"),
        "projectId" : os.getenv("projectId"),
        "messagingSenderId" : os.getenv("messagingSenderId"),
        "appId" : os.getenv("appId"),
    }

    return render(request, "patient_notifications.html", context)