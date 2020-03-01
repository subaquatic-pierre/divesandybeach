from django.contrib import admin
from .models import (DiveSite, MarineLife, DiveTrip, DiveTripInfo, Course,
                     CourseInfo, ItemPrice, Image, Category)
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


admin.site.register(DiveSite, DiveSiteAdmin)
admin.site.register(MarineLife, MarineLifeAdmin)
admin.site.register(DiveTrip)
admin.site.register(DiveTripInfo)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInfo)
admin.site.register(ItemPrice, ItemPriceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category)
