from django.test import TestCase, Client
from diving.models import Course, CourseBookingRequest, CourseBookingExtraDivers
from django.shortcuts import reverse
from django.forms import formset_factory
import os
from django.http import HttpRequest
from diving.forms import (
    CourseBookingDivers,
    CourseBookingRequestForm,
)
from django.core import mail


class CoursesTest(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        self.client = Client()
        self.courses = Course.objects.all()

    def test_course_list_view_status(self):
        """ Check that all course detail pages return 200 OK """
        for course in self.courses:
            url = reverse('diving:padi-course-detail', args=(course.slug, ))
            response = self.client.get(url)

    def test_course_list_entry_level(self):
        """ Test entry level is on course list page """
        entry_level = Course.objects.filter(level__title='Entry Level')
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertQuerysetEqual(
            entry_level, response.context['entry_level'], transform=lambda x: x, ordered=False)

    def test_course_list_advanced_level(self):
        """ Test advanced level is on course list page """
        advanced_level = Course.objects.filter(level__title='Advanced Level')
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertQuerysetEqual(
            advanced_level, response.context['advanced_level'], transform=lambda x: x, ordered=False)

    def test_course_list_specialties(self):
        """ Test specialty level is on course list page """
        specialties = Course.objects.filter(level__title='Specialty Courses')
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertQuerysetEqual(
            specialties, response.context['specialties'], transform=lambda x: x, ordered=False)

    def test_course_list_pro_level(self):
        """ Test professional level is on course list page """
        pro_level = Course.objects.filter(level__title='Professional Level')
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertQuerysetEqual(
            pro_level, response.context['pro_level'], transform=lambda x: x, ordered=False)

    def test_course_list_tec_rec(self):
        """ Test technical level is on course list page """
        tecrec_level = Course.objects.filter(level__title='TecRec Level')
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertQuerysetEqual(
            tecrec_level, response.context['tecrec_level'], transform=lambda x: x, ordered=False)

    def test_course_list_title(self):
        """ Ensure correct title of course list """
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertEqual('PADI Courses', response.context['title'])

    def test_course_list_seo_description(self):
        """ Ensure correct seo description of course list """
        response = self.client.get(reverse('diving:padi-course-list'))
        self.assertEqual(
            'Full Range Of PADI Courses | PADI 5 Star IDC Resort |  From Entry Level Courses to PADI Profesional Programs, Sign Up With A PADI Instructor Today!',
            response.context['seo_description'])

    def test_course_detail_title(self):
        """ Test title in PADI course detail view """
        course = Course.objects.all().first()
        url = reverse('diving:padi-course-detail', args=(course.slug, ))
        response = self.client.get(url)
        self.assertEqual(course.title, response.context['title'])

    def test_course_detail_description(self):
        """ Ensure SEO description is sent to course detail view"""
        course = Course.objects.all().first()
        url = reverse('diving:padi-course-detail', args=(course.slug, ))
        response = self.client.get(url)
        self.assertEqual(course.title, response.context['title'])

    def test_course_detail_seo_keywords(self):
        """ Test seo_keywords in PADI course detail view """
        course = Course.objects.all().first()
        url = reverse('diving:padi-course-detail', args=(course.slug, ))
        response = self.client.get(url)
        self.assertEqual(course.seo_keywords, response.context['seo_keywords'])


class CourseBooking(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        os.environ['RECAPTCHA_DISABLE'] = 'True'
        self.client = Client(
            HTTP_REFERER='https://divesandybeach.com/padi-courses/open-water-diver/')
        self.extra_divers = [
            'First Diver',
            'Second Diver',
            'Third Diver',
            'Fourth Diver',
        ]

        self.form_user_input = {
            'email': 'test@test.com',
            'course': 'Open Water Diver',
            'date': '2020-10-30',
            'message': 'This is a test message',
        }

        self.post_user_input = {
            'form-TOTAL_FORMS': '4',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-full_name': self.extra_divers[0],
            'form-1-full_name': self.extra_divers[1],
            'form-2-full_name': self.extra_divers[2],
            'form-3-full_name': self.extra_divers[3],
            'email': 'test@test.com',
            'course': 'Open Water Diver',
            'date': '2020-10-30',
            'message': 'This is a test message',
        }

    def test_initial_state_form(self):
        """ Test the course booking form is preselected with the course page from which the request came """
        response = self.client.get(reverse('diving:course-booking-request'))
        form = response.context['form']
        self.assertEqual(form.initial['course'], 'Open Water Diver')

    def test_title(self):
        """ Test the title of the course booking page """
        response = self.client.get(reverse('diving:course-booking-request'))
        self.assertEqual(
            response.context['title'], 'PADI Course Booking Request')

    def test_diver_form(self):
        """ Test diver form is passed into template is correct form """
        formset = formset_factory(CourseBookingDivers)
        response = self.client.get(reverse('diving:course-booking-request'))
        self.assertEqual(
            response.context['diver_form'].__name__, formset.__name__)

    def test_valid_course_booking_request(self):
        """ Validate data being passed into the post request creates valid form """
        data = self.form_user_input
        form = CourseBookingRequestForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_data_post(self):
        data = self.post_user_input
        data['form-0-full_name'] = ''
        data['form-1-full_name'] = ''
        data['form-2-full_name'] = ''
        data['form-3-full_name'] = ''
        response = self.client.post(
            reverse('diving:course-booking-request'), data)
        form = CourseBookingRequestForm()
        DiverFormSet = formset_factory(CourseBookingDivers)
        divers_formset = DiverFormSet()
        message = str(list(response.context['messages'])[0])
        self.assertEqual(
            message, "Sorry, your input was not valid, please try again")
        self.assertEqual(
            response.context['form'].__name__, form.__name__)
        self.assertEqual(
            str(type(response.context['diver_form'])), str(type(divers_formset)))

    def test_valid_object_input(self):
        """ Test a valid course booking object is created on form submit """
        data = self.post_user_input
        divers = self.extra_divers
        response = self.client.post(
            reverse('diving:course-booking-request'), data)
        course_booking = CourseBookingRequest.objects.get(full_name=divers[0],
                                                          email=data['email'],
                                                          course=data['course'],
                                                          )
        self.assertTrue(course_booking)

    def test_all_divers_in_object(self):
        """ Test all divers are associated with the course booking request """
        data = self.post_user_input
        divers = self.extra_divers
        response = self.client.post(
            reverse('diving:course-booking-request'), data)
        course_booking = CourseBookingRequest.objects.get(full_name=divers[0],
                                                          email=data['email'],
                                                          course=data['course'],
                                                          )
        new_divers = CourseBookingExtraDivers.objects.filter(
            course_booking=course_booking.id)
        for i, new_diver in enumerate(new_divers):
            self.assertEqual(new_diver.full_name, divers[i])

    def test_staff_email(self):
        """ Test email is sent to staff on form submit """
        data = self.post_user_input
        divers = self.extra_divers
        response = self.client.post(
            reverse('diving:course-booking-request'), data)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], 'info@divesandybeach.com')

    def test_customer_email(self):
        """ Test email is sent to customer on form submit """
        data = self.post_user_input
        divers = self.extra_divers
        response = self.client.post(
            reverse('diving:course-booking-request'), data)
        email = mail.outbox[1]
        self.assertEqual(email.to[0], data['email'])
