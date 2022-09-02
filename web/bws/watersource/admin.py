from watersource.models import WaterSource
from django.contrib import admin

# Register your models here.


@admin.register(WaterSource)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ['identification', 'description',  'latitude',
                    'longitude', 'datetime_creation', 'deleted']  # 'geolocation',
    list_filter = ['datetime_creation']
