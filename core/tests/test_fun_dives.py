from django.test import TestCase, Client
from django.shortcuts import reverse
from django.utils.text import slugify
from diving.models import DiveTrip, ItemPrice, DiveBookingRequest, DiveBookingRequestDiver
from django.core import mail
from django.forms import formset_factory
import os
from django.utils.dateparse import parse_date

from diving.forms import (
    DiveBookingRequestForm,
    DiveBookingRequestDiverForm,
    BoatDiveBookingRequestForm,
    ShoreDiveBookingRequestForm
)


class FunDiveTests(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        self.client = Client()

    def test_boat_dive_title(self):
        """ Ensure boat dive title in boat dive view """
        dive = DiveTrip.objects.get(slug='fujairah-boat-dive')
        url = reverse('diving:fun-diving', args=('fujairah-boat-dive', ))
        response = self.client.get(url)
        self.assertEqual(dive.title, response.context['title'])

    def test_boat_dive_seo_description(self):
        """ Test description in boat dive """
        dive = DiveTrip.objects.get(slug='fujairah-boat-dive')
        url = reverse('diving:fun-diving', args=('fujairah-boat-dive', ))
        response = self.client.get(url)
        self.assertEqual(dive.seo_description,
                         response.context['seo_description'])

    def test_boat_dive_seo_keywords(self):
        """ Test keywords in boat dive """
        dive = DiveTrip.objects.get(slug='fujairah-boat-dive')
        url = reverse('diving:fun-diving', args=('fujairah-boat-dive', ))
        response = self.client.get(url)
        self.assertEqual(dive.seo_keywords, response.context['seo_keywords'])

    def test_boat_dive_price(self):
        """ Test correct price is in boat diving view """
        dive = DiveTrip.objects.get(slug='fujairah-boat-dive')
        filter_text = slugify(dive.title)
        prices = ItemPrice.objects.filter(trip_type=filter_text)
        url = reverse('diving:fun-diving', args=('fujairah-boat-dive', ))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            prices, response.context['prices'], transform=lambda x: x, ordered=False)

    def test_shore_dive_title(self):
        """ Ensure shore dive title in shore dive view """
        dive = DiveTrip.objects.get(slug='dive-snoopy-island')
        url = reverse('diving:fun-diving', args=('dive-snoopy-island', ))
        response = self.client.get(url)
        self.assertEqual(dive.title, response.context['title'])

    def test_shore_dive_seo_description(self):
        """ Test description in shore dive """
        dive = DiveTrip.objects.get(slug='dive-snoopy-island')
        url = reverse('diving:fun-diving', args=('dive-snoopy-island', ))
        response = self.client.get(url)
        self.assertEqual(dive.seo_description,
                         response.context['seo_description'])

    def test_shore_dive_seo_keywords(self):
        """ Test keywords in shore dive """
        dive = DiveTrip.objects.get(slug='dive-snoopy-island')
        url = reverse('diving:fun-diving', args=('dive-snoopy-island', ))
        response = self.client.get(url)
        self.assertEqual(dive.seo_keywords, response.context['seo_keywords'])

    def test_shore_dive_price(self):
        """ Test correct price is in shore diving view """
        dive = DiveTrip.objects.get(slug='dive-snoopy-island')
        filter_text = slugify(dive.title)
        prices = ItemPrice.objects.filter(trip_type=filter_text)
        url = reverse('diving:fun-diving', args=('dive-snoopy-island', ))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            prices, response.context['prices'], transform=lambda x: x, ordered=False)


class FunDiveBooking(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        os.environ['RECAPTCHA_DISABLE'] = 'True'
        self.client = Client()
        self.divers = [
            {'full_name': 'First User',
             'cert_level': 'Junior Scuba Diver',
             'kit_required': 'Full Kit'},
            {'full_name': 'Second User',
             'cert_level': 'Open Water',
             'kit_required': 'Tanks and Weights'}
        ]
        self.user_input = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-full_name': self.divers[0]['full_name'],
            'form-0-cert_level': self.divers[0]['cert_level'],
            'form-0-kit_required': self.divers[0]['kit_required'],
            'email': 'test@test.com',
            'date': '04/15/2020',
            'message': 'Test message'
        }

    def test_get_shore_diving_form(self):
        """ Test that shore diving form is rendered when refered from shore dive """
        client = Client(HTTP_REFERER='dive-snoopy-island/')
        form = ShoreDiveBookingRequestForm()
        response = client.get(reverse('diving:booking-request'))
        self.assertEqual(form.__name__, response.context['heading'])

    def test_get_boat_diving_form(self):
        """ Test that boat diving form is rendered when refered from page any thing other than shore diving """
        client = Client()
        form = BoatDiveBookingRequestForm()
        response = response = client.get(reverse('diving:booking-request'))
        self.assertEqual(form.__name__, response.context['heading'])

    def test_valid_boat_diver_form_input(self):
        """ Test valid message when diver submits valid data into boat dive booking form """
        user_input = self.user_input
        user_input['boat_time'] = '9am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Booking request success!')

    def test_invalid_boat_dive_booking_form_username(self):
        """ Test correct message is shown if a user does not enter their name """
        user_input = self.user_input
        user_input['form-0-full_name'] = ''
        user_input['boat_time'] = '9am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        self.assertFormsetError(
            response, 'diver_form', 0, 'full_name', 'This field is required.')

    def test_valid_shore_dive_form(self):
        """ Ensure shore dive is valid  """
        data = {
            'email': self.user_input['email'],
            'date': self.user_input['date'],
            'message': self.user_input['message'],
            'shore_time': '10am',
            'shore': 'shore'
        }
        booking_form = ShoreDiveBookingRequestForm(data=data)
        self.assertTrue(booking_form.is_valid())

    def test_valid_boat_dive_form(self):
        """ Ensure boat dive form is valid  """
        data = {
            'email': self.user_input['email'],
            'date': self.user_input['date'],
            'message': self.user_input['message'],
            'boat_time': '9am'
        }
        booking_form = BoatDiveBookingRequestForm(data=data)
        self.assertTrue(booking_form.is_valid())

    def test_divers_booking_form(self):
        """ Test divers booking form works with more than one divers """
        diver1 = self.divers[0]
        diver2 = self.divers[1]
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-full_name': diver1['full_name'],
            'form-0-cert_level': diver1['cert_level'],
            'form-0-kit_required': diver1['kit_required'],
            'form-1-full_name': diver2['full_name'],
            'form-1-cert_level': diver2['cert_level'],
            'form-1-kit_required': diver2['kit_required'],
        }
        DiverFormSet = formset_factory(
            DiveBookingRequestDiverForm, validate_min=True, min_num=1)
        divers_formset = DiverFormSet(data=data)
        self.assertTrue(divers_formset.is_valid())

    def test_shore_dive_object(self):
        """ Test successfull creation of valid shore dive object on shore dive form submit """
        diver1 = self.divers[0]
        user_input = self.user_input
        user_input['shore'] = 'shore'
        user_input['shore_time'] = '10am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        shore_dive = DiveBookingRequest.objects.get(full_name=diver1['full_name'],
                                                    email=user_input['email'],
                                                    trip_type='shore-dive',
                                                    time='10am',
                                                    message=user_input['message'],
                                                    closed=False,
                                                    )
        self.assertTrue(shore_dive)

    def test_shore_dive_object_divers(self):
        """ Test successfull creation of valid shore dive object on shore dive form submit and all divers are added to request """
        diver1 = self.divers[0]
        diver2 = self.divers[1]
        user_input = self.user_input
        user_input['shore'] = 'shore'
        user_input['shore_time'] = '10am'
        user_input['form-TOTAL_FORMS'] = '2'
        user_input['form-1-full_name'] = diver2['full_name']
        user_input['form-1-cert_level'] = diver2['cert_level']
        user_input['form-1-kit_required'] = diver2['kit_required']
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        shore_dive = DiveBookingRequest.objects.get(full_name=diver1['full_name'],
                                                    email=user_input['email'],
                                                    trip_type='shore-dive',
                                                    time='10am',
                                                    message=user_input['message'],
                                                    closed=False,
                                                    )
        divers = DiveBookingRequestDiver.objects.all()
        divers_shore_dive = DiveBookingRequestDiver.objects.filter(
            dive_booking_query=shore_dive.id)
        self.assertQuerysetEqual(
            divers, divers_shore_dive, ordered=False, transform=lambda x: x)

    def test_boat_dive_object(self):
        """ Test successfull and valid creation of boat dive object on valid form submit """
        """ Test successfull creation of valid shore dive object on shore dive form submit """
        diver = self.divers[0]
        user_input = self.user_input
        user_input['boat_time'] = '9am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        boat_dive = DiveBookingRequest.objects.get(full_name=diver['full_name'],
                                                   email=user_input['email'],
                                                   trip_type='boat-dive',
                                                   time='9am',
                                                   message=user_input['message'],
                                                   closed=False,
                                                   )
        self.assertTrue(boat_dive)

    def test_boat_dive_staff_email(self):
        """ Test success send of staff email on boat dive form submit """
        diver = self.divers[0]
        user_input = self.user_input
        user_input['boat_time'] = '9am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], 'info@divesandybeach.com')

    def test_boat_dive_customer_email(self):
        """ Test successfully sent customer email on valid boat dive form submit """
        diver = self.divers[0]
        user_input = self.user_input
        user_input['boat_time'] = '9am'
        response = self.client.post(
            reverse('diving:booking-request'), user_input)
        email = mail.outbox[1]
        self.assertEqual(email.to[0], user_input['email'])
