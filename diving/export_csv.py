from django.http import HttpResponse
import csv


class ExportCSV:
    def export_as_csv(self, request, queryset, field_names=None):
        if field_names:
            field_names = field_names
        else:
            field_names = []
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        label = meta.label_lower.split('.')
        filename = f'{label[0]}_{label[1]}.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        writer = csv.writer(response)
        # Check model type to ensure proper export
        if filename == 'diving_course.csv':
            writer.writerow(field_names)
            for obj in queryset:
                item = [getattr(obj, field)
                        for field in field_names]
                row = writer.writerow(item)
            return response

    export_as_csv.short_description = 'Export Selected'


class ExportCourses(ExportCSV):
    def export_as_csv(self, request, queryset):
        field_names = ['title', 'level', 'min_age', 'duration',
                       'num_pool_dives', 'num_ocean_dives', 'minimum_certiication_level',
                       'schedule', 'description']
        return super().export_as_csv(request, queryset, field_names)


class ExportItemPrices(ExportCSV):
    def export_as_csv(self, request, queryset):
        field_names = ['title', 'category', 'price']
        return super().export_as_csv(request, queryset, field_names)


class ExportDiveSites(ExportCSV):
    def export_as_csv(self, request, queryset):
        field_names = ['title', 'category', 'price']
        return super().export_as_csv(request, queryset, field_names)


class ExportDiveSites(ExportCSV):
    def export_as_csv(self, request, queryset):
        field_names = ['title', 'min_diver_level', 'site_type',
                       'dive_time', 'distance', 'depth', 'info']
        return super().export_as_csv(request, queryset, field_names)
