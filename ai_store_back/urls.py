from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            ("authentication.urls", "authentication"),
            namespace="authentication",
        ),
    ),
    path(
        "api/",
        include(("neural_network.urls", "neural_network"), namespace="neural_network"),
    ),
    path("api/", include(("swagger.urls", "swagger"), namespace="swagger")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
