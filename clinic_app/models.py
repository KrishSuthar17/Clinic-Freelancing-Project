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

