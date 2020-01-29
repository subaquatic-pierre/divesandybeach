from django.contrib import admin
from .models import (DiveSite, MarineLife, DiveTrip, DiveTripInfo, Course,
                     CourseInfo, CourseFAQ, ItemPrice, Images, Category)
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
        'learning_type',
        'trip_type',
        'price'

    ]

    list_filter = [
        'category'
    ]

    search_fields = [
        'title',
    ]


admin.site.register(DiveSite, DiveSiteAdmin)
admin.site.register(MarineLife, MarineLifeAdmin)
admin.site.register(DiveTrip)
admin.site.register(DiveTripInfo)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInfo)
admin.site.register(CourseFAQ)
admin.site.register(ItemPrice, ItemPriceAdmin)
admin.site.register(Images)
admin.site.register(Category)
