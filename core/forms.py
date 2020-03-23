from django import forms
from django.forms import ModelForm, Form
from .models import ContactUsRequest
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter divers full name'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    message = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Send us a message'}))
    captcha = ReCaptchaField()
