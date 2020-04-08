from django.test import TestCase, Client, RequestFactory
from django.shortcuts import reverse
from pprint import pprint
from django.http import HttpRequest
from core.views import Home, ContactPageView
from core.forms import ContactForm
from django.core import mail
import re
import os
from core.models import ContactUsRequest
from diving.models import DiveSite, Course, DiveTrip, ItemPrice
from django.core import management
from django.utils.text import slugify


# Home page

core_app_urls = [
    '/',
    '/fujairah-dive-centre-about-us/',
    '/amazing-scuba-diving-contact-us/',
]


class CorePageTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_seo(self):
        """ Test all core pages have seo tags in the header """
        for url in core_app_urls:
            response = self.client.get(path=url)
            self.assertContains(response, text='<title>')
            self.assertContains(response, text='<meta property="og:image"')
            self.assertContains(
                response, text='<meta name="keywords" content=')
            self.assertContains(
                response, text='<meta name="description" content=')


class ContactPage(TestCase):
    def setUp(self):
        os.environ['RECAPTCHA_DISABLE'] = 'True'
        self.contact_request = ContactUsRequest.objects.create(
            full_name='Jarred Tester', email='admin@tester.com', message='Testing message for test suite')
        self.client = Client()
        self.request_factory = RequestFactory()

    def test_valid_input(self):
        """ Test valid contact form input """
        user_input = {
            'full_name': 'James Jones',
            'email': 'the@best.email',
            'message': 'This is a test, from the most awesome test suite',
        }
        form = ContactForm(data=user_input)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """ Test invalid email input fails """
        user_input = {
            'full_name': 'James Jones',
            'email': 'the@',
            'message': 'This is a test, from the most awesome test suite',
        }
        response = self.client.post(
            '/amazing-scuba-diving-contact-us/', user_input)
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')

    def test_username_required(self):
        """ Test username required on contact form """
        user_input = {
            'full_name': '',
            'email': 'the@best.test',
            'message': 'This is a test, from the most awesome test suite',
        }
        response = self.client.post(
            '/amazing-scuba-diving-contact-us/', user_input)
        self.assertFormError(response, 'form', 'full_name',
                             'This field is required.')

    def test_contact_model_creation(self):
        """ Test contact model is created on form submit """
        user_input = {
            'full_name': 'James Tester',
            'email': 'the@best.test',
            'message': 'This is a test, from the most awesome test suite',
        }
        response = self.client.post(
            '/amazing-scuba-diving-contact-us/', user_input)
        model = ContactUsRequest.objects.get(
            full_name=user_input['full_name'],
            email=user_input['email'],
            message=user_input['message']
        )
        self.assertTrue(model)

    def test_update_contact_response(self):
        """ Update the contact us object created when staff follows link to update contact request to reponded to """
        contact_request = self.contact_request
        request = HttpRequest()
        url = reverse('core:update-contact-us', args=(contact_request.id, ))
        response = self.client.get(url)

        # refetch object from DB to check status
        updated_contact_request = ContactUsRequest.objects.get(
            id=contact_request.id)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(updated_contact_request.responded, True)

    def test_plain_text_customer_email(self):
        """ Email is sent to customer on contact form submit, with correct data """
        user_input = {
            'full_name': 'James Tester',
            'email': 'the@best.test',
            'message': 'This is a test, from the most awesome test suite',
        }
        first_name = user_input['full_name'].split()[0]
        response = self.client.post(
            '/amazing-scuba-diving-contact-us/', user_input)

        email = mail.outbox[0]
        # Use regex to find name in email body
        pattern = re.compile(r'(Hi )([a-zA-Z]*)')
        mo = pattern.search(email.body)
        email_name = mo.group(2)
        email_address = email.to[0]
        email_subject = email.subject

        self.assertEqual(email_address, user_input['email'])
        self.assertEqual(email_name, first_name)
        self.assertEqual(email_subject, 'Contact Us')

    def test_html_staff_email(self):
        """ Email is sent to staff on contact form submit, with correct data """
        user_input = {
            'full_name': 'James Tester',
            'email': 'the@best.test',
            'message': 'This is a test, from the most awesome test suite',
        }
        first_name = user_input['full_name'].split()[0]
        response = self.client.post(
            '/amazing-scuba-diving-contact-us/', user_input)

        email = mail.outbox[1]
        email_address = email.to[0]
        email_subject = email.subject

        self.assertInHTML(
            f""" <h4>Diver Name: {user_input['full_name']}</h4> """, email.body)
        self.assertEqual(email_address, 'info@divesandybeach.com')
        self.assertEqual(email_subject, 'Contact Us')


class PriceTest(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        self.client = Client()

    def test_all_item_prices(self):
        """ Test all item prices are in the price page """
        prices = ItemPrice.objects.all()
        response = self.client.get(reverse('diving:prices'))
        self.assertQuerysetEqual(
            prices, response.context['object'], ordered=False, transform=lambda x: x)
