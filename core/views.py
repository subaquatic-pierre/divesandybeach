from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.core.mail import send_mail
from diving.email import CustomerEmail
from .models import ContactUsRequest


class Home(TemplateView):
    template_name = 'core/index.html'


class AboutUs(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        context['seo_description'] = 'About Us | PADI 5 Star IDC Resort | Daily diving trips, PADI courses and diving equipment, join us for the best diving in Fujairah!'
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
            # messages.info(
            #     request, 'Sorry, your input was not valid, please try again')
            return render(request, 'core/contact.html', context={'form': info})
        else:
            name = info.cleaned_data['full_name']
            email = info.cleaned_data['email']
            message = info.cleaned_data['message']

            # Create contact request for the database
            contact_request = ContactUsRequest.objects.create(
                full_name=name,
                email=email,
                message=message
            )

            context = {
                'full_name': name,
                'email': email,
                'message': message,
                'url': request.build_absolute_uri(reverse('core:update-contact-us', args=(contact_request.id, ))),
                'contact': True,
                'contact_subject': 'Contact Us'
            }

            # Send customer email
            customer_email = CustomerEmail([], context)
            customer_email.send()
            contact_request.save()

            # Send email with message to staff
            msg = render_to_string(
                'diving/email/contact_us_request.html', context=context)
            send_mail('Contact Us', msg, 'info@divesandybeach.com',
                      ['info@divesandybeach.com'], html_message=msg)

            # messages.info(request, 'Thank you for contacting us!')
            return render(request, 'diving/booking_success.html')


class SiteMapView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/sitemap.xml', content_type="application/xhtml+xml")


@csrf_exempt
def update_contact_us(request, pk):
    if request.method == 'GET':
        data = request.POST
        contact_request = ContactUsRequest.objects.get(pk=pk)
        contact_request.responded = True
        contact_request.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse('Bad request', status=400)


""" TODO
- update-contact-us view, redirect on successful update of model
 """
