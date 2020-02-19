from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from .forms import ContactForm
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.core.mail import send_mail
from diving.email import CustomerEmail


class Home(TemplateView):
    template_name = 'core/index.html'


class AboutUs(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        return context


class ContactPageView(View):

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'title': 'Contact Us',
                   'form': form}

        return render(request, 'core/contact.html', context=context)

    def post(self, request, *args, **kwargs):
        info = ContactForm(request.POST)

        if not info.is_valid():
            messages.info(
                request, 'Sorry, your input was not valid, please try again')
            return render(request, 'diving/course_booking_request.html', context={'form': info})
        else:

            name = info.cleaned_data['full_name']
            email = info.cleaned_data['email']
            message = info.cleaned_data['message']
            context = {
                'full_name': name,
                'email': email,
                'message': message,
                'contact': True,
                'contact_subject': 'Contact Us'
            }

            customer_email = CustomerEmail([], context)
            customer_email.send()

            msg = render_to_string(
                'diving/email/contact_us_request.html', context=context)
            send_mail('Contact Us', msg, 'info@divesandybeach.com',
                      ['info@divesandybeach.com'], html_message=msg)

            messages.info(request, 'Thank you for contacting us!')
            return render(request, 'diving/booking_success.html')


""" TODO
- Change delay on front page animation
- add padding between dive pages
- Pool, Ocean, Book learning, E-Learning info content
 """
