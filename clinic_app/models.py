from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
import uuid
from django.utils.timezone import now

# Create your models here.

class testimonials_reviews(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True,blank=True)
    Title_of_your_review = models.CharField(max_length=100,null=False)
    Your_review = models.TextField(max_length=200,null=True)
    Your_name = models.CharField(max_length=50)
    Your_email = models.CharField(null=False,max_length=120)
    expr = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Your_name

class faq(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200,null=False)
    answer = models.TextField(max_length=1000,null=False)

    def __str__(self):
        return self.question
    

class gallery(models.Model):
    title = models.CharField(max_length=100,null=False)
    youtube_id = models.CharField(max_length=300,null=False)

    def __str__(self):
        return f"Image {self.title}"
    
class blog(models.Model):
    id = models.AutoField(primary_key=True)
    min_title = models.CharField(max_length=200,null=False)
    title = models.CharField(max_length=200,null=False)
    slug = models.SlugField(max_length=255,null=True,blank=True,unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    content = models.TextField(max_length=5000,null=False)
    image = models.ImageField(upload_to='media/', null=False, default="doctor-hero.jpg")
    author = models.CharField(max_length=100,null=False,default="Dr. Ketul Soni")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class contact_gallary(models.Model):
    image = models.ImageField(upload_to='media/', null=False, default="doctor-hero.jpg")
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    specialization = models.TextField()
    image = models.ImageField(upload_to="doctors/", null=False, default="doctor-hero.jpg")
    is_active = models.BooleanField(default=True)

    
    about_title = models.CharField(max_length=200)
    about_subtitle = models.CharField(max_length=200, blank=True)
    about_points = models.TextField(
        help_text="Enter each point on a new line"
    )
    def __str__(self):
        return self.name
    
class DoctorLeave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.doctor.name} Leave from {self.start_date} to {self.end_date}"
    

class ClinicHoliday(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Holiday on {self.date} - {self.reason}"


# diseases/models.py
class Disease(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="diseases/")
    slug = models.SlugField(max_length=100, unique=True, default="Disease")
    description = models.TextField(max_length=2500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name


# videos/models.py
class LiveSession(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# settings/models.py
class ClinicInfo(models.Model):
    clinic_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    address = models.TextField()
    tagline = models.CharField(max_length=200)

    about_heading = models.CharField(max_length=200)   
    about_text = models.TextField()                    

    def __str__(self):
        return "Clinic Info"



class HomeopathyAbout(models.Model):
    heading = models.CharField(max_length=200)
    points = models.TextField(
        help_text="Har line ek bullet point hogi"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading
    

class Homeopathy_start_about_content(models.Model):
    about_heading = models.CharField(max_length=200)   
    about_text = models.TextField()      

    def __str__(self):
        return "Homeopathy_start_about_content"

class Homeopathy_end_about_content(models.Model):
    about_heading = models.CharField(max_length=200)   
    about_text = RichTextField()

    def __str__(self):
        return "Homeopathy_end_about_content"
    


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    patient_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^[6-9]\d{9}$', 'Invalid phone number')]
    )
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateField()
    time_slot =models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    # DATA RETENTION FIELDS
    is_anonymized = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    anonymized_at = models.DateTimeField(null=True, blank=True)

    idempotency_key = models.UUIDField(unique=True, editable=False,default=uuid.uuid4,)

    class Meta:
        unique_together = ('doctor', 'date', 'time_slot')

    def save(self, *args, **kwargs):
        if not self.idempotency_key:
            self.idempotency_key = uuid.uuid4()
        super().save(*args, **kwargs)


class Device(models.Model):
    USER_TYPE = [
        ('doctor','Doctor'),
        ('patient','Patient')
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    phone = models.CharField(max_length=15, null=True, blank=True)  
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )    
    fcm_token = models.TextField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Doctor uniqueness
            models.UniqueConstraint(
                fields=["user_type", "user", "fcm_token"],
                name="unique_doctor_device",
                condition=models.Q(user_type="doctor")
            ),
            # Patient uniqueness
            models.UniqueConstraint(
                fields=["user_type", "phone", "fcm_token"],
                name="unique_patient_device",
                condition=models.Q(user_type="patient")
            ),
        ]

    def __str__(self):
        return f"{self.user_type} – {self.fcm_token[:10]}"
    

class Notification(models.Model):
    RECIPIENT = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    recipient_type = models.CharField(max_length=10, choices=RECIPIENT)
    recipient_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=False,blank=False, default="")
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    




class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('BOOK_ATTEMPT', 'Book Attempt'),
        ('BOOK_SUCCESS', 'Book Success'),
        ('BOOK_FAIL', 'Book Fail'),
        ('OTP_SENT', 'OTP Sent'),
        ('OTP_VERIFIED', 'OTP Verified'),
        ('RATE_LIMIT_BLOCK', 'Rate Limit Block'),
        ('CAPTCHA_FAIL', 'Captcha Fail'),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.action} - {self.phone}"
    

class RateLimit(models.Model):
    phone = models.CharField(max_length=15)
    ip_address = models.GenericIPAddressField()
    count = models.PositiveIntegerField(default=0)
    window_start = models.DateTimeField()


class ClinicSchedule(models.Model):
    weekly_off_days = models.JSONField(default=list, blank=True)
    special_closed_dates = models.JSONField(default=list, blank=True)
    special_open_dates = models.JSONField(default=list, blank=True)

    def __str__(self):
        return "Clinic Schedule"
