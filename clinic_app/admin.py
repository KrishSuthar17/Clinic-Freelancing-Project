from django.contrib import admin
from .models import testimonials_reviews,faq,gallery,blog,contact_gallary
# Register your models here.

admin.site.register(testimonials_reviews)
class testimonials_reviewsAdmin(admin.ModelAdmin):
    list_display = ('Your_name','Title_of_your_review','rating','created_at')
    search_fields = ('Your_name','Title_of_your_review','Your_email')

admin.site.register(faq)
class faqAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)

admin.site.register(gallery)
class galleryAdmin(admin.ModelAdmin):
    list_display = ('title','link')
    search_fields = ('title',)

admin.site.register(blog)
class blogAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at')
    search_fields = ('title','author')


admin.site.register(contact_gallary)
class contact_gallaryAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)
