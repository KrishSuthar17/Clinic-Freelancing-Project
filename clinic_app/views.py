from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, "home.html")

def homeopathy_page(request):
    return render(request, "homeopathy_page.html")

def online_consultation_page(request):
    return render(request, "online_consultation_page.html")

def testimonials_page(request):
    return render(request, "testimonials_page.html")

def faqs_page(request):
    return render(request, "faqs_page.html")

def gallery_videos_page(request):
    return render(request, "gallery_videos_page.html")

def blogs_page(request):
    return render(request, "blogs_page.html")

def content(request):
    return render(request, "content.html")