from django.contrib import admin
from .models import (
    DiveSite,
    MarineLife,
    DiveTrip,
    DiveTripInfo,
    Course,
    CourseInfo,
    ItemPrice, Image,
    Category,
    DiveBookingRequest,
    DiveBookingRequestDiver,
    CourseBookingRequest,
    CourseBookingExtraDivers
)
from .export_csv import ExportCourses, ExportItemPrices, ExportDiveSites

from django.http import HttpResponse
import csv


class DiveSiteAdmin(admin.ModelAdmin):
    change_list_template = 'diving/divesites_changelist.html'
    actions = ['export_as_csv']

    list_display = [
        'title',
    ]

    list_filter = [
    ]

    search_fields = [
        'title',
    ]


class CourseAdmin(admin.ModelAdmin, ExportCourses):
    change_list_template = 'diving/courses_changelist.html'
    actions = ['export_as_csv']

    list_display = [
        'title',
        'level',
    ]

    list_filter = [
        'level'
    ]

    search_fields = [
        'title',
    ]


class MarineLifeAdmin(admin.ModelAdmin):
    pass


class ItemPriceAdmin(admin.ModelAdmin, ExportItemPrices):
    change_list_template = 'diving/itemsprices_changelist.html'
    actions = ['export_as_csv']

    list_display = [
        'title',
        'category',
        'course',
        'trip_type',
        'price'
    ]

    list_filter = [
        'category'
    ]

    search_fields = [
        'title',
    ]


class ImageAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]

    list_display = [
        'title',
        'admin_thumbnail'
    ]


class DiveBookingRequestDiverInline(admin.TabularInline):
    model = DiveBookingRequestDiver

    extra = 1


class DiveBookingRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'email',
        'trip_type',
        'time',
        'date',
        'closed',
    ]

    inlines = [DiveBookingRequestDiverInline, ]

    list_filter = [
        'full_name',
        'trip_type',
        'time',
        'date',
        'closed',
    ]


class DiveBookingRequestDiverAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'cert_level',
        'kit_required',
        'dive_booking_query',
    ]

    search_filter = [
        'full_name',
    ]

    list_filter = [
        'dive_booking_query',
    ]


class CourseBookingRequestDiverInline(admin.TabularInline):
    model = CourseBookingExtraDivers

    extra = 1


class CourseBookingRequestAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'course',
        'email',
        'date',
        'closed',
    ]

    list_filter = [
        'course',
        'date'
    ]

    inlines = [CourseBookingRequestDiverInline, ]


class CourseBookingRequestDiverAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
    ]

    search_filter = [
        'full_name',
    ]

    list_filter = [
        'course_booking',
    ]


admin.site.register(CourseBookingRequest, CourseBookingRequestAdmin)
admin.site.register(CourseBookingExtraDivers, CourseBookingRequestDiverAdmin)
admin.site.register(DiveBookingRequest, DiveBookingRequestAdmin)
admin.site.register(DiveBookingRequestDiver, DiveBookingRequestDiverAdmin)
admin.site.register(DiveSite, DiveSiteAdmin)
admin.site.register(MarineLife, MarineLifeAdmin)
admin.site.register(DiveTrip)
admin.site.register(DiveTripInfo)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInfo)
admin.site.register(ItemPrice, ItemPriceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
