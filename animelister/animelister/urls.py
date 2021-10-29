from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from django.contrib import admin
from urllib.parse import urlparse

urlpatterns = [
    path("accounts/", include("animelister.user.urls")),
    path("admin/", admin.site.urls),
    path("", include("animelister.home.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    media_url = urlparse(settings.MEDIA_URL).path
    urlpatterns += static(media_url, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path(r"__debug__/", include(debug_toolbar.urls))]
