from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from .forms import ContactForm
from django.contrib.messages.views import SuccessMessageMixin


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
        if info.is_valid():
            name = info.cleaned_data['full_name']
            email = info.cleaned_data['email']
            message = info.cleaned_data['message']

            # TODO: Send email to user and staff
        form = ContactForm()
        messages.success(request, 'Thank you for contacting us!')
        return render(request, 'core/contact.html', context={'form': form})
