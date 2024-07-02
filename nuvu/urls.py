"""
URL configuration for nvc_crm project.
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from nuvu import settings

admin.site.site_header = 'Nuvu Administration'
admin.site.site_title = 'Nuvu Admin Panel'
admin.site.index_title = 'Nuvu Dashboard'

schema_view = get_schema_view(
    openapi.Info(
        title="NuVu Conair API",
        default_version="v1",
        description="API doc",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="het.vaghasia@tecblic.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("", include("apps.user.urls")),
    path("ticket/", include("apps.ticket.urls")),
    path("whatsapp/", include("apps.whatsapp.urls")),
    path("catalogue/", include("apps.catalogue.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
