from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.AboutUs.as_view(), name='about-us'),
    path('contact/', views.ContactPageView.as_view(), name='contact-us')
]
