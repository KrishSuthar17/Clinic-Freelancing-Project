from django.shortcuts import render

from clinic_app.models import ClinicInfo, Disease, Doctor, HomeopathyAbout, LiveSession
from .forms import testimonials_reviews_forms
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

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
    }
    return render(request, "homeopathy_page.html",context)

def online_consultation_page(request):
    context = {
        "doctor": Doctor.objects.filter(is_active=True).first(),
    }
    return render(request, "online_consultation_page.html",context)

def testimonials_page(request):
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

    return render(request, "testimonials_page.html", {"form": form})

# views.py

def faq_page(request):
    faqs = [
        {
            "question": "What is homeopathy?",
            "answer": (
                "Homeopathy, a system used for over 200 years, works on the principle "
                "that 'like cures like' — an illness is treated with a substance that "
                "could produce similar symptoms in a healthy person. However, medicines "
                "are given in highly diluted forms and are therefore extremely safe and "
                "have no side effects."
            ),
            "open": True,  # first one open
        },
        {
            "question": "What is a homeopathic consultation like?",
            "answer": "A homeopathic consultation is detailed and individualized...",
            "open": False,
        },
        {
            "question": "What is a constitutional treatment in homeopathy?",
            "answer": "Constitutional treatment focuses on the person as a whole...",
            "open": False,
        },
        {
            "question": "Unique nature of homeopathic prescription",
            "answer": "Each prescription is unique to the individual...",
            "open": False,
        },
        {
            "question": "How does a homeopath choose the potency?",
            "answer": "Potency is chosen based on multiple factors...",
            "open": False,
        },
    ]

    return render(request, "faqs_page.html", {"faqs": faqs})


def gallery_videos_page(request):
    return render(request, "gallery_videos_page.html")

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

    return render(request, "blogs_page.html", {"doctor": doctor})

def content(request):
    return render(request, "content.html")
