from django.db import models
from django.contrib.auth.models import AbstractUser

CERT_LEVEL_CHOICES = (
    ('OW', "Open Water"),
    ('AOW', "Advanced Open Water"),
    ('RD', "Rescue Diver"),
    ('DM', "Dive Master"),
    ('INST', "Instructor"),
)


class User(AbstractUser):
    USER_NAME = 'email'
    cert_level = models.CharField(max_length=255, choices=CERT_LEVEL_CHOICES)


class ContactUsRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.email + ' - ' + self.date.strftime('%y%m%D')

    class Meta:
        verbose_name_plural = 'Contact Queries'
