from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ContactUsRequest


class ContactUsRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'email',
        'date',
        'responded'
    ]


admin.site.register(User, UserAdmin)
admin.site.register(ContactUsRequest, ContactUsRequestAdmin)
