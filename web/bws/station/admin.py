from django.contrib import admin
from station.models import Sensor, Station, StationType, SensorStation, SensorValue, AlertSensor

# Register your models here.


@admin.register(StationType)
class StationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key',)
    fields = ('name', 'key',)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('identification', 'station_type',
                    'datetime_creation', 'latitude', 'longitude',)
    fields = ('identification', 'station_type',
              'description', 'latitude', 'longitude',)


@admin.register(Sensor)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'graphic_type')
    fields = ('name', 'key', 'graphic_type')


@admin.register(SensorStation)
class SensorTypeStationAdmin(admin.ModelAdmin):
    list_display = ('station', 'sensor_type')
    fields = ('station', 'sensor_type')


@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = ('station', 'sensor_type', 'sensor_value',
                    'datetime_collected', 'datetime_creation', 'from_api')
    fields = ('station', 'sensor_type', 'sensor_value',
              'datetime_collected', 'from_api')


@admin.register(AlertSensor)
class AlertSensorAdmin(admin.ModelAdmin):
    list_display = ('station', 'sensor_type', 'user', 'operator',
                    'main_value', 'second_value', 'time_frequency', 'datetime_creation')
    fields = ('station', 'sensor_type', 'user', 'operator',
              'main_value', 'second_value', 'time_frequency', 'prev_exec')
