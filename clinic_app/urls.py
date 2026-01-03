from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('homeopathy/', homeopathy_page, name='homeopathy'),
    path('online_consultation/', online_consultation_page, name='online_consultation'),
    path('testimonials/', testimonials_page, name='testimonials'),
    path('faqs/', faq_page, name='faqs'),
    path('gallery_videos/', gallery_videos_page, name='gallery_videos'),
    path('blogs/', blogs_page, name='blogs'),
    path('content/', content, name='content'),
    path("diseases/<slug:slug>/", disease_page, name="disease_detail"),
    path('blogs/<slug:slug>/', blog_detail, name='blog_detail'),
    path("book/", book_appointment, name="book"),
    path("confirm/<int:appointment_id>/", confirm_appointment, name="confirm"),
]