from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    # TODO: Create namespace for each app
    path("", include("diving.urls", namespace="diving")),
    path("", include("core.urls", namespace="core")),
    path("accounts/", include("allauth.urls")),
]


# if settings.DEBUG == False:
#     STATIC_ROOT = os.path.join(settings.BASE_DIR, "static")
#     urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# TODO: Customize admin check SDD urls.py
# TODO: Add url pattern for static and media root check SDD urls.py
