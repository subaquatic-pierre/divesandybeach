from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views import View
from django.forms import formset_factory
from .models import DiveSite, Category, Course, DiveTrip, ItemPrice
from .forms import UploadCSVForm, CourseBookingRequestForm, DiveBookingRequestForm, DiveBookingRequestDiverForm
from .upload_csv import UploadDiveSitesCSV, UploadItemPrice, UploadCoursesCSV
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import Context


class DiveSiteListView(ListView):
    model = DiveSite
    context_object_name = 'dive_sites'
    template_name = 'diving/dive_site_list.html'


class DiveSiteDetailView(DetailView):
    model = DiveSite
    context_object_name = 'site'
    template_name = 'diving/dive_site_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        return context


class PADICourseLevelListView(ListView):
    model = Category
    context_object_name = 'course_levels'
    template_name = 'diving/padi_course_level_list.html'


class PADICourseLevelDetailView(DetailView):
    model = Category
    context_object_name = 'course_level'
    template_name = 'diving/padi_course_level_detail.html'

    def get_context_data(self, **kwargs):
        courses = Course.objects.filter(level__title=kwargs['object'])
        context = super().get_context_data(**kwargs)
        context['courses'] = courses
        context['title'] = context['object'].title
        return context


class PADICourseListView(View):
    def get(self, request, *args, **kwargs):

        entry_level = Course.objects.filter(level__title='Entry Level')
        advanced_level = Course.objects.filter(level__title='Advanced Level')
        specialties = Course.objects.filter(level__title='Specialty Courses')
        pro_level = Course.objects.filter(level__title='Professional Level')
        tecrec_level = Course.objects.filter(level__title='TecRec Level')
        context = {'entry_level': entry_level,
                   'advanced_level': advanced_level,
                   'specialties': specialties,
                   'pro_level': pro_level,
                   'tecrec_level': tecrec_level}

        return render(request, 'diving/all_padi_courses.html', context=context)


class PADICourseDetailView(DetailView):
    model = Course
    template_name = 'diving/padi_course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        return context


class BoatDiveDetailView(TemplateView):
    template_name = 'diving/boat_diving.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dive'] = DiveTrip.objects.get(title='Boat Diving')
        context['title'] = 'Fujairah Boat Diving'

        return context


class ShoreDiveDetailView(TemplateView):
    template_name = 'diving/shore_diving.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dive'] = DiveTrip.objects.get(title='Shore Diving')
        context['title'] = 'Fujairah Shore Diving'

        return context


class PricesDetailView(TemplateView):
    template_name = 'diving/prices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = ItemPrice.objects.all()
        context['title'] = 'Prices'
        context['categories'] = Category.objects.all()
        context['title'] = 'Price List'
        return context


class BookingRequestView(View):
    def get(self, request, *args, **kwargs):
        booking_form = DiveBookingRequestForm()
        diver_form = formset_factory(DiveBookingRequestDiverForm)
        context = {'booking_form': booking_form,
                   'diver_form': diver_form,
                   'title': 'Dive Booking Request'}
        return render(request, 'diving/booking_request.html', context=context)

    def post(self, request, *args, **kwargs):
        booking_form = DiveBookingRequestForm(request.POST)
        DiverFormSet = formset_factory(DiveBookingRequestDiverForm)
        divers = DiverFormSet(request.POST)
        print(request.POST)

        if divers.is_valid():
            print('\n\nDivers Data:')
            print(divers.cleaned_data)
        else:
            print('\n\nDivers form is not valid')
            print(request.POST)
            print('\n\n')
            messages.warning(request, 'Form is not valid, please try again')
            return render(request, 'diving/booking_request.html', context={'booking_form': booking_form, 'diver_form': divers})

        if booking_form.is_valid():
            print('\n\Booking Form Data:')
            print(booking_form.cleaned_data)
            print('\n\n')
            # return render(request, 'diving/booking_success.html')
        else:
            print('\n\nBooking Form Data is not valid')
            print(request.POST)
            print('\n\n')
            return render(request, 'diving/booking_request.html', context={'booking_form': booking_form, 'diver_form': divers})

        # else:
            # messages.warning(request, 'Form is not valid, please try again')
            # return redirect('diving:booking-request')
        return redirect('diving:booking-request')


class CourseBookingRequestView(View):
    def get(self, request, *args, **kwargs):
        # Build course title from refering URL
        url = request.META.get('HTTP_REFERER')
        last = url.split('/')[len(url.split('/'))-2].split('-')
        last = ' '.join(last).title()
        print(last)
        form = CourseBookingRequestForm(
            initial={'course': last})
        context = {'form': form,
                   'title': 'PADI Course Booking Request'}
        return render(request, 'diving/course_booking_request.html', context=context)

    def post(self, request, *args, **kwargs):
        form = CourseBookingRequestForm(request.POST)
        # Get form data
        if form.is_valid():
            diver_name = form.cleaned_data['full_name']
            date = form.cleaned_data['date']
            course = form.cleaned_data['course']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            extra_divers = []
            # Get extra divers if there are
            for k, v in form.cleaned_data.items():
                if k.startswith('extra_diver'):
                    extra_divers.append(v)

            # Send email
            # TODO: Email customer and staff
            # Create back link to to send confirmation email from staff email
            email_message = f""" 

            This is the email message:
            -------------------------
            Diver Name: {diver_name}
            -------------------------
            Diver Emaiil: {email}
            -------------------------
            Course: {course}
            -------------------------
            Date Requested: {date}
            -------------------------
            Message: {message}
            -------------------------
            Extra Divers: {extra_divers}

             """
            send_mail('Course Bookiing Request', email_message, 'subquatic.pierre@gmail.com', [
                      email, 'subquatic.pierre@gmail.com'])
            # print(f'\n\nDiver Name: {diver_name}')
            # print(f'Email: {email}')
            # print(f'Course: {course}')
            # print(f'Date: {date}')
            # print(f'Message: {message}')
            # print(f'Extra divers include:')
            # for diver in extra_divers:
            #     print(diver)
            # print('\n\n')
            return render(request, 'diving/booking_success.html')
        else:
            messages.warning(request, 'Form is not valid, please try again')
            return render(request, 'diving/course_booking_request.html', context={'form': form})


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


def dive_booking_email(request):
    # Get email details
    subject = 'Dive Booking Confirmation'
    to_email = 'subaqautic.pierre@gmail.com'
    from_email = 'subaqautic.pierre@gmail.com'
    staff_email = 'subaqautic.pierre@gmail.com'
    diver_name = 'Eric Poper'
    extra_divers = ['Garry Benson', 'Henri mcitosh']
    context = {'diver_name': diver_name,
               'extra_divers': extra_divers}
    msg_html = render_to_string(
        'diving/dive_booking_confirmation.html', context)
    msg_plain = render_to_string(
        'diving/dive_booking_confirmation.txt', context)
    # Send email
    send_mail(subject, msg_plain, from_email, [
              to_email, staff_email], html_message=msg_html)

    return render(request, 'diving/dive_booking_confirmation.html', context=context)


"""
TODO:

- Design email templates for booking request
- Add breadcrumbs to course detail and dive site detail page
- design boat diving page
- design shore diving page

"""
