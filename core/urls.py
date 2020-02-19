from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('fujairah-dive-centre-about-us/',
         views.AboutUs.as_view(), name='about-us'),
    path('amazing-scuba-diving-contact-us/',
         views.ContactPageView.as_view(), name='contact-us')
]
