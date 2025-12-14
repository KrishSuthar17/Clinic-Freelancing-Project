from django.contrib import admin
from .models import testimonials_reviews
# Register your models here.

admin.site.register(testimonials_reviews)
class testimonials_reviewsAdmin(admin.ModelAdmin):
    list_display = ('Your_name','Title_of_your_review','rating','created_at')
    search_fields = ('Your_name','Title_of_your_review','Your_email')