from django.views import View
from .upload_csv import UploadDiveSitesCSV, UploadItemPrice, UploadCoursesCSV
from .forms import UploadCSVForm
from django.shortcuts import render, redirect
from django.contrib import messages


class UploadItemPrices(View):
    def get(self, request, *args, **kwargs):
        form = UploadCSVForm()
        context = {'form': form}
        return render(request, "diving/upload_csv_form.html", context)

    def post(self, request, *args, **kwargs):
        form = UploadCSVForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = request.FILES['csv_file']
            # Check iif CSV file
            if not file.name.endswith('.csv'):
                messages.info(request, 'This s not a CSV file')
                return redirect('admin:diving_itemprice_changelist')
            # Upload csv file function in shop/utisl.py
            upload_items = UploadItemPrice()
            if upload_items.upload(file):
                messages.info(request, 'File successfully uploaded')
                return redirect('admin:diving_itemprice_changelist')
            else:
                # TODO: Improve upload_shop_data error checking in shop/views.py
                messages.warning(request, 'File upload unsucessful')
                return redirect('admin:diving_itemprice_changelist')
        else:
            messages.info(request, 'Invalid file format')
            return redirect('admin:diving_itemprice_changelist')


class UploadCourses(View):
    def get(self, request, *args, **kwargs):
        form = UploadCSVForm()
        context = {'form': form}
        return render(request, "diving/upload_csv_form.html", context)

    def post(self, request, *args, **kwargs):
        form = UploadCSVForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = request.FILES['csv_file']
            # Check iif CSV file
            if not file.name.endswith('.csv'):
                messages.info(request, 'This s not a CSV file')
                return redirect('admin:diving_course_changelist')
            # Upload csv file function in shop/utisl.py
            upload_courses = UploadCoursesCSV()
            if upload_courses.upload(file):
                messages.info(request, 'File successfully uploaded')
                return redirect('admin:diving_course_changelist')
            else:
                # TODO: Improve upload_shop_data error checking in shop/views.py
                messages.warning(request, 'File upload unsucessful')
                return redirect('admin:diving_course_changelist')
        else:
            messages.info(request, 'Invalid file format')
            return redirect('admin:diving_course_changelist')


class UploadDiveSites(View):
    def get(self, request, *args, **kwargs):
        form = UploadCSVForm()
        context = {'form': form}
        return render(request, "diving/upload_csv_form.html", context)

    def post(self, request, *args, **kwargs):
        form = UploadCSVForm(request.POST, request.FILES or None)
        if form.is_valid():
            file = request.FILES['csv_file']
            # Check iif CSV file
            if not file.name.endswith('.csv'):
                messages.info(request, 'This s not a CSV file')
                return redirect('admin:diving_divesite_changelist')
            # Upload csv file function in shop/utisl.py
            upload_dive_sites = UploadDiveSitesCSV()
            if upload_dive_sites.upload(file):
                messages.info(request, 'File successfully uploaded')
                return redirect('admin:diving_divesite_changelist')
            else:
                # TODO: Improve upload_shop_data error checking in shop/views.py
                messages.warning(request, 'File upload unsucessful')
                return redirect('admin:diving_divesite_changelist')
        else:
            messages.info(request, 'Invalid file format')
            return redirect('admin:diving_divesite_changelist')
