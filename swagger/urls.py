from django.urls import include, path, re_path

from rest_framework.permissions import AllowAny

from drf_yasg.openapi import Contact, Info
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    Info(
        title="AI Store Backend API",
        default_version="v1",
        description="Данный проект является частью программной инфраструктуры ai_store. "
        + "Это веб-приложение обеспечивает клиенту доступ к ИС и другим веб-приложениям. "
        + "Всю информацию об API приложения можно узнать в соотвествии со спецификацией OpenAPI.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=Contact(email="muhtarullin450@gmail.com"),
    ),
    patterns=[
        path("api/", include("neural_network.urls")),
        path("api/", include("authentication.urls")),
    ],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "redoc-old/",
        schema_view.with_ui("redoc-old", cache_timeout=0),
        name="schema-redoc-old",
    ),
    re_path(
        r"^cached/swagger(?P<format>.json|.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="cschema-json",
    ),
    path(
        "cached/swagger/",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="cschema-swagger-ui",
    ),
    path(
        "cached/redoc/",
        schema_view.with_ui("redoc", cache_timeout=None),
        name="cschema-redoc",
    ),
]
