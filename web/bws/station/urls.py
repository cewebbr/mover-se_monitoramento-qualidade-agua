from django.urls import path
from . import views

app_name = 'station'

urlpatterns = [
    path('sensor/new-value/', views.newSensorValue, name='new_sensor_value'),
    path('sensor/new-value/ajax/sensor/', views.sensorAjax, name='sensor_ajax'),
    path('alert/', views.alert, name='alert'),
    path('delete/<int:id>', views.deleteAlert, name='delete_alert'),
    path('alert/ajax/sensor/', views.sensorAjax, name='sensor_ajax'),
    path('<int:id>/', views.stationDetail, name='station_detail'),
    path('<int:id>/ajax/sensor/', views.sensorValuesAjax, name='sensorValuesAjax'),
    path('<int:id_station>/sensor/<str:id_sensor>/',
         views.sensorDetail, name='sensor_detail'),
]
