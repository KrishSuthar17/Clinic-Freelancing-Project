from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    content = models.TextField(max_length=5000,null=False)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    author = models.CharField(max_length=100,null=False,default="Dr. Ketul Soni")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class contact_gallary(models.Model):
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    
# doctors/models.py
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    specialization = models.TextField()
    image = models.ImageField(upload_to="doctors/")
    is_active = models.BooleanField(default=True)

    
    about_title = models.CharField(max_length=200)
    about_subtitle = models.CharField(max_length=200, blank=True)
    about_points = models.TextField(
        help_text="Enter each point on a new line"
    )
    def __str__(self):
        return self.name


# diseases/models.py
class Disease(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="diseases/")
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
    
from ckeditor.fields import RichTextField
class Homeopathy_end_about_content(models.Model):
    about_heading = models.CharField(max_length=200)   
    about_text = RichTextField()

    def __str__(self):
        return "Homeopathy_end_about_content"
    

