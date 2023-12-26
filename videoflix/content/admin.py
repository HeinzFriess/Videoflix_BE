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


from content.admin import VideoResource
import json  

def exportBackUp():
	dataset = VideoResource().export()
	with open("VideoResourceBackUp.json", "w") as save_file: 
	    json.dump(dataset.json , save_file, indent = 6)
    #save_file.close()

def importBackUp():
    with open("VideoResourceBackUp.json") as json_file:
        data = json.load(json_file)