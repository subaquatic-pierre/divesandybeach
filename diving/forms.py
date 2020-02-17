from django import forms
from django.forms.widgets import Select
from .models import CourseBookingRequest, DiveBookingRequest, Course, CERT_LEVEL_CHOICES, TRIP_TIME_CHOICES, EQUIPMENT_CHOICES
from tempus_dominus.widgets import DatePicker
from .widgets import KitSelectWidget, CertLevelSelectWidget

BLANK_CHOICE = [
    ('', 'Select cert level')
]

CERT_CHOICE = (BLANK_CHOICE) + list(CERT_LEVEL_CHOICES)

# print(CERT_CHOICE)


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()


class CourseBookingRequestForm(forms.Form):
    COURSES = Course.objects.all()
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    course = forms.ChoiceField(choices=[(course.title, course.title) for course in list(COURSES)], widget=forms.Select(
                               attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    date = forms.DateField(
        widget=DatePicker(
            options={
                'icons': {
                    'next': 'fas fa-chevron-right',
                    'previous': 'fas fa-chevron-left',
                },
                'useCurrent': False,
            }, attrs={
                'input_toggle': True,
                'input_group': False,
                'autocomplete': 'off'
            }
        )
    )

    message = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Send us a message'}))


class CourseBookingDivers(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter divers full name'}))


class DiveBookingRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter your email address'}))
    date = forms.DateField(
        widget=DatePicker(
            options={
                # 'format': 'd m Y',
                'icons': {
                    'next': 'fas fa-chevron-right',
                    'previous': 'fas fa-chevron-left',
                },
                'useCurrent': False,
            }, attrs={
                'input_toggle': True,
                'input_group': False,
                'autocomplete': 'off'
            }
        )
    )
    message = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Send us a message'}))


class DiveBookingRequestDiverForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter diver full name'}))
    cert_level = forms.TypedChoiceField(required=True, choices=CERT_LEVEL_CHOICES, widget=CertLevelSelectWidget(
        attrs={'class': 'form-control', 'required': True}))
    kit_required = forms.TypedChoiceField(required=True, choices=EQUIPMENT_CHOICES, widget=KitSelectWidget(
        attrs={'class': 'form-control', 'required': True}))


class BoatDiveBookingRequestForm(DiveBookingRequestForm):
    time = forms.ChoiceField(required=True, choices=TRIP_TIME_CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'custom-control-input'}))

    @property
    def __name__(self):
        return 'Boat Dive'


class ShoreDiveBookingRequestForm(DiveBookingRequestForm):
    time = forms.ChoiceField(required=True, choices=(('10AM', '10AM'), ('0AM', '0AM'),), widget=forms.RadioSelect(
        attrs={'class': 'custom-control-input'}))
    shore = forms.CharField(
        required=False, widget=forms.HiddenInput(attrs={'value': 'shore'}))
    # TODO: Add time picker to shore dives

    @property
    def __name__(self):
        return 'Shore Dive'
