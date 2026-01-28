from django import forms
from .models import testimonials_reviews

class testimonials_reviews_forms(forms.ModelForm):
    class Meta:
        model = testimonials_reviews
        fields = ['rating','Title_of_your_review','Your_review','Your_name','Your_email','expr']
        labels = {'expr': 'I confirm that This review is based on my own experience and is my genuine opinion.'} 
        widgets = {
            'Title_of_your_review': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Summarize your review'
            }),
            'Your_review': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 5,
                'placeholder': 'Tell people your review'
            }),
            'Your_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Your name'
            }),
            'Your_email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Your email'
            }),
            'expr': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4'
            }),
        }