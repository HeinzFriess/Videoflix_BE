from django.contrib import admin
from content.models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
#@admin.register(Video, VideoAdmin)
class VideoAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Video,VideoAdmin)
