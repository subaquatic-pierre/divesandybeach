from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.text import slugify
from django.views.generic import FormView
from django.views import View
from django.forms import formset_factory
from .models import (
    DiveSite,
    Category,
    Course,
    DiveTrip,
    ItemPrice,
    DiveBookingRequest,
    DiveBookingRequestDiver,
    CourseBookingRequest,
    CourseBookingExtraDivers,
)
from .forms import (
    CourseBookingDivers,
    UploadCSVForm,
    CourseBookingRequestForm,
    DiveBookingRequestForm,
    DiveBookingRequestDiverForm,
    BoatDiveBookingRequestForm,
    ShoreDiveBookingRequestForm,
)
from django.contrib import messages
from django.template.loader import render_to_string
from django.template import Context
from .email import StaffEmail, CustomerEmail, CourseStaffEmail


class DiveSiteListView(ListView):
    model = DiveSite
    context_object_name = "dive_sites"
    template_name = "diving/dive_site_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Fujairah Dive Sites"
        context[
            "seo_description"
        ] = "Check out our dive sites along the Fujairah coastline. Each site offering abundant marine life, ranging from ship wrecks to beautiful coral reef."
        context["seo_keywords"] = "Fujairah Dive Sites, Scuba Dive Fujairah"
        return context


class DiveSiteDetailView(DetailView):
    model = DiveSite
    context_object_name = "site"
    template_name = "diving/dive_site_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["object"].title
        context["seo_description"] = context["object"].seo_description
        context["seo_keywords"] = context["object"].seo_keywords
        return context


class PADICourseLevelListView(ListView):
    model = Category
    context_object_name = "course_levels"
    template_name = "diving/padi_course_level_list.html"


class PADICourseLevelDetailView(DetailView):
    model = Category
    context_object_name = "course_level"
    template_name = "diving/padi_course_level_detail.html"

    def get_context_data(self, **kwargs):
        courses = Course.objects.filter(level__title=kwargs["object"])
        context = super().get_context_data(**kwargs)
        context["courses"] = courses
        context["title"] = context["object"].title
        return context


class PADICourseListView(View):
    def get(self, request, *args, **kwargs):

        entry_level = Course.objects.filter(level__title="Entry Level")
        advanced_level = Course.objects.filter(level__title="Advanced Level")
        specialties = Course.objects.filter(level__title="Specialty Courses")
        pro_level = Course.objects.filter(level__title="Professional Level")
        tecrec_level = Course.objects.filter(level__title="TecRec Level")
        context = {
            "entry_level": entry_level,
            "advanced_level": advanced_level,
            "specialties": specialties,
            "pro_level": pro_level,
            "tecrec_level": tecrec_level,
            "title": "PADI Courses",
            "seo_description": "Full Range Of PADI Courses | PADI 5 Star IDC Resort |  From Entry Level Courses to PADI Profesional Programs, Sign Up With A PADI Instructor Today!",
        }

        return render(request, "diving/all_padi_courses.html", context=context)


class PADICourseDetailView(DetailView):
    model = Course
    template_name = "diving/padi_course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["object"].title
        context["seo_description"] = context["object"].seo_description
        context["seo_keywords"] = context["object"].seo_keywords
        return context


class DiveDetailView(DetailView):
    model = DiveTrip
    template_name = "diving/fun_diving.html"
    context_object_name = "dive"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["object"].title
        context["seo_description"] = context["object"].seo_description
        context["seo_keywords"] = context["object"].seo_keywords
        price_filter = slugify(context["title"])
        context["prices"] = ItemPrice.objects.filter(trip_type=price_filter)

        return context


class PricesDetailView(TemplateView):
    template_name = "diving/prices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = ItemPrice.objects.all()
        context["title"] = "Prices"
        context["categories"] = Category.objects.all()
        context["seo_descrition"] = (
            "Prices | Discover | Experience | PADI 5 Star IDC Resort | Daily Diving Trips, PADI Courses And Diving Equipment, Join Us For The The Best Diving In Fujairah!",
        )
        context["title"] = "Price List"
        return context


class BookingRequestView(View):
    def get(self, request, *args, **kwargs):
        referer = request.META.get("HTTP_REFERER")
        try:
            if referer.endswith("dive-snoopy-island/"):
                booking_form = ShoreDiveBookingRequestForm()
            else:
                booking_form = BoatDiveBookingRequestForm()
        except Exception:
            # Referer is none type, default to boat diving form
            booking_form = BoatDiveBookingRequestForm()

        diver_form = formset_factory(DiveBookingRequestDiverForm, validate_min=True)

        context = {
            "booking_form": booking_form,
            "diver_form": diver_form,
            "title": "Dive Booking Request",
            "heading": booking_form.__name__,
        }

        return render(request, "diving/booking_request.html", context=context)

    def post(self, request, *args, **kwargs):
        shore = request.POST.get("shore", None)
        if shore:
            booking_form = ShoreDiveBookingRequestForm(request.POST)
        else:
            booking_form = BoatDiveBookingRequestForm(request.POST)

        DiverFormSet = formset_factory(
            DiveBookingRequestDiverForm, validate_min=True, min_num=1
        )
        divers_formset = DiverFormSet(request.POST)

        context = {
            "booking_form": booking_form,
            "diver_form": divers_formset,
            "title": "Dive Booking Request",
            "heading": booking_form.__name__,
        }
        # print(booking_form)
        # print(divers_formset)

        if not divers_formset.is_valid() or not booking_form.is_valid():
            messages.info(request, "Sorry, your input was not valid, please try again")
            return render(request, "diving/booking_request.html", context=context)

        else:

            # Both forms are valid, construct email, only send email after successfull model creations
            divers = divers_formset.cleaned_data
            booking_info = booking_form.cleaned_data
            booking_info["subject"] = "Dive booking request"
            booking_info["dive_type"] = booking_form.__name__
            staff_email = StaffEmail(divers, booking_info)
            customer_email = CustomerEmail(divers, booking_info)

            # Set dive time based on dive trip type
            if booking_info["dive_type"] == "Boat Dive":
                time = booking_info["boat_time"]
            else:
                time = booking_info["shore_time"]

            # Create booking request
            booking_request = DiveBookingRequest(
                full_name=divers[0]["full_name"],
                email=booking_info["email"],
                trip_type=slugify(booking_info["dive_type"]),
                time=time,
                date=booking_info["date"],
                message=booking_info["message"],
            )
            booking_request.save()

            # Create diver and add them to booking request
            for diver in divers:
                new_diver = DiveBookingRequestDiver(
                    full_name=diver["full_name"],
                    cert_level=diver["cert_level"],
                    kit_required=diver["kit_required"],
                    dive_booking_query=booking_request,
                )
                new_diver.save()

            # New data saved to database, send emails
            staff_email.send()
            customer_email.send()

            messages.success(request, "Booking request success!")
            return render(request, "diving/booking_success.html")


class CourseBookingRequestView(View):
    def get(self, request, *args, **kwargs):
        # Build course title from refering URL
        url = request.META.get("HTTP_REFERER")
        last = url.split("/")[len(url.split("/")) - 2].split("-")
        last = " ".join(last).title()
        form = CourseBookingRequestForm(initial={"course": last})

        diver_form = formset_factory(CourseBookingDivers)
        context = {
            "form": form,
            "diver_form": diver_form,
            "title": "PADI Course Booking Request",
        }

        return render(request, "diving/course_booking_request.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CourseBookingRequestForm(request.POST)
        DiverFormSet = formset_factory(
            CourseBookingDivers, validate_min=True, min_num=1
        )
        divers_formset = DiverFormSet(request.POST)
        # print(form)
        # print(divers_formset)

        context = {
            "form": form,
            "diver_form": divers_formset,
            "title": "PADI Course Booking Request",
        }

        if not divers_formset.is_valid() or not form.is_valid():
            messages.info(request, "Sorry, your input was not valid, please try again")
            return render(
                request, "diving/course_booking_request.html", context=context
            )

        else:
            # Both forms are valid, construct and send email
            booking_info = form.cleaned_data
            divers = divers_formset.cleaned_data
            booking_info["subject"] = "Course booking request"
            booking_info["dive_type"] = "course"
            booking_info["course"] = booking_info["course"]

            staff_email = CourseStaffEmail(divers, booking_info)
            customer_email = CustomerEmail(divers, booking_info)

            # Create course booking object
            diver_name = divers[0].get("full_name")
            date = booking_info.get("date")
            message = booking_info.get("message")
            email = booking_info.get("email")
            course = booking_info.get("course")
            course_booking = CourseBookingRequest(
                full_name=diver_name,
                email=email,
                course=course,
                date=date,
                message=message,
            )
            course_booking.save()
            for diver in divers:
                new_diver = CourseBookingExtraDivers(full_name=diver.get("full_name"))
                new_diver.course_booking = course_booking
                new_diver.save()

            staff_email.send()
            customer_email.send()

            messages.success(request, "Booking request success!")
            return render(request, "diving/booking_success.html")


"""
TODO:

- Change course info pictures, pool, boat, shore, classroom
- create booking entry when someone submits a booking

"""
