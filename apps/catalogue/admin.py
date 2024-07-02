from django.contrib import admin
from apps.catalogue.models import Catalogue, Visitor
from import_export.admin import ExportActionMixin
from django.http import HttpResponse
from django.core.files.storage import default_storage
import zipfile
from django.utils.text import slugify
from io import BytesIO
# Register your models here.


# admin.site.register(Catalogue)
# admin.site.register(Visitor)


# class Catalogue(admin.ModelAdmin):
#     fields = "__all__"

# class CatalogueAdmin(ExportActionMixin, admin.ModelAdmin):
#     list_display = ("name", "qr_image", "urls", "created_at")

# admin.site.register(Catalogue, CatalogueAdmin)


def download_qr_images(modeladmin, request, queryset):
    zip_filename = f"{slugify(modeladmin.model.__name__)}_qr_images.zip"
    in_memory_zip = BytesIO()

    with zipfile.ZipFile(in_memory_zip, 'w') as archive:
        for obj in queryset:
            if obj.qr_image:
                image_path = obj.qr_image.path
                archive.write(image_path, f"{slugify(obj.name)}_{obj.id}.png")

    in_memory_zip.seek(0)
    response = HttpResponse(in_memory_zip, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    return response

download_qr_images.short_description = "Download selected QR images as zip"

class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('name', 'qr_image', 'urls', 'created_at')
    actions = [download_qr_images]

admin.site.register(Catalogue, CatalogueAdmin)


class VisitorAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("catalogue_fk", "name", "email", "mobile", "company_name", "created_at")

admin.site.register(Visitor, VisitorAdmin)