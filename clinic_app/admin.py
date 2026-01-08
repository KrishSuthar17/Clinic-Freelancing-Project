from django.contrib import admin
from .models import testimonials_reviews,faq,gallery,blog,contact_gallary,Appointment,Notification
from clinic_app.utils.notifications import notify_patient_cancellation, notify_patient_confirmation
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

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'date', 'time_slot', 'status')
    list_filter = ('doctor', 'status', 'date')
    search_fields = ('patient_name', 'phone')

    def save_model(self, request, obj, form, change):
        old_status = None

        if obj.pk:
            old_status = Appointment.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        # 🔥 SEND NOTIFICATION ONLY ON STATUS CHANGE → confirmed
        if old_status != "confirmed" and obj.status == "confirmed":
            print("🔥 ADMIN CONFIRM → SENDING PATIENT NOTIFICATION")
            notify_patient_confirmation(obj)
        
        # ❌ CANCEL
        if old_status != "cancelled" and obj.status == "cancelled":
            print("🔥 ADMIN → CANCEL")
            notify_patient_cancellation(obj)
    
    readonly_fields = ("patient_name", "phone")

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_anonymized:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient_type", "title", "is_read", "created_at")
    list_filter = ("recipient_type", "is_read")
    search_fields = ("title", "message")


# admin.py (all apps)
from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(Disease)
admin.site.register(LiveSession)
admin.site.register(ClinicInfo)
admin.site.register(HomeopathyAbout)
admin.site.register(Homeopathy_start_about_content)
admin.site.register(Homeopathy_end_about_content)
