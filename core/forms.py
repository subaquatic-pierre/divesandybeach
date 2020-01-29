from django import forms
from django.forms import ModelForm
from .models import ContactUsRequest


class ContactForm(ModelForm):
    class Meta:
        model = ContactUsRequest
        fields = ['full_name', 'email', 'message']
