from django.urls import path
from . import views

app_name = 'diving'


urlpatterns = [
    path('fujairah-dive-site/',
         views.DiveSiteListView.as_view(), name='dive-site-list'),
    path('fujairah-dive-site/<slug>/',
         views.DiveSiteDetailView.as_view(), name='dive-site-detail'),
    path('padi-level/',
         views.PADICourseLevelListView.as_view(), name='course-level-list'),
    path('padi-level/<slug>/',
         views.PADICourseLevelDetailView.as_view(), name='course-level-detail'),
    path('padi-courses/',
         views.PADICourseListView.as_view(), name='padi-course-list'),
    path('padi-level/<level_slug>/<slug>/',
         views.PADICourseDetailView.as_view(), name='padi-course-detail'),
    path('boat-diving/',
         views.BoatDiveDetailView.as_view(), name='boat-diving'),
    path('shore-diving/',
         views.ShoreDiveDetailView.as_view(), name='shore-diving'),
    path('prices/',
         views.PricesDetailView.as_view(), name='prices'),
    path('course-booking-request/',
         views.CourseBookingRequestView.as_view(), name='course-booking-request'),
    path('booking-request/',
         views.BookingRequestView.as_view(), name='booking-request'),
    path('upload-item-price/', views.UploadItemPrices.as_view(),
         name='upload-item-price'),
    path('upload-courses/', views.UploadCourses.as_view(),
         name='upload-courses'),
    path('upload-dive-sites/', views.UploadDiveSites.as_view(),
         name='upload-dive-sites'),
]
