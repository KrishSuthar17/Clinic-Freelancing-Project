from django.shortcuts import render
from .forms import testimonials_reviews_forms
from django.contrib import messages
from django.shortcuts import redirect
from .models import faq, testimonials_reviews, gallery, blog, contact_gallary

# Create your views here.

def home_page(request):
    return render(request, "home.html")

def homeopathy_page(request):
    return render(request, "homeopathy_page.html")

def online_consultation_page(request):
    return render(request, "online_consultation_page.html")

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
