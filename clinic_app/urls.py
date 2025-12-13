from django.urls import path
from .views import home_page, homeopathy_page,blogs_page,content,faqs_page,gallery_videos_page,online_consultation_page,testimonials_page

urlpatterns = [
    path('', home_page, name='home'),
    path('homeopathy/', homeopathy_page, name='homeopathy'),
    path('online_consultation/', online_consultation_page, name='online_consultation'),
    path('testimonials/', testimonials_page, name='testimonials'),
    path('faqs/', faqs_page, name='faqs'),
    path('gallery_videos/', gallery_videos_page, name='gallery_videos'),
    path('blogs/', blogs_page, name='blogs'),
    path('content/', content, name='content'),
]