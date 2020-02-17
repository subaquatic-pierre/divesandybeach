from django.urls import path
from . import views
from . import upload_utils

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
    path('padi-courses/<slug>/',
         views.PADICourseDetailView.as_view(), name='padi-course-detail'),
    path('fun-diving/<slug>/',
         views.DiveDetailView.as_view(), name='fun-diving'),
    path('prices/',
         views.PricesDetailView.as_view(), name='prices'),
    path('course-booking-request/',
         views.CourseBookingRequestView.as_view(), name='course-booking-request'),
    path('booking-request/',
         views.BookingRequestView.as_view(), name='booking-request'),
    path('upload-item-price/', upload_utils.UploadItemPrices.as_view(),
         name='upload-item-price'),
    path('upload-courses/', upload_utils.UploadCourses.as_view(),
         name='upload-courses'),
    path('upload-dive-sites/', upload_utils.UploadDiveSites.as_view(),
         name='upload-dive-sites'),
]
