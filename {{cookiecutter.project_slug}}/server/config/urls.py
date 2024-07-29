from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin

from apps.geo.routes import APP_PREFIX as GEO_PREFIX

API_PREFIX = ""

urlpatterns = [
    re_path(settings.ADMIN_URL, admin.site.urls),
    # path(API_PREFIX, include("apps.auth.routes")),
    # path(API_PREFIX, include("apps.users.routes")),
    path(API_PREFIX + GEO_PREFIX, include("apps.geo.routes")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 