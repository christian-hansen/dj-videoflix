from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from .models import Video


# Register your models here.
class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportActionModelAdmin):
    pass
