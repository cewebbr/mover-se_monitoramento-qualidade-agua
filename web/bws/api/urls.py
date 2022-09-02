from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('post_sensor_value', views.postSensorValue, name='postSensorValue'),
]
