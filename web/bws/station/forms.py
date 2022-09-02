from django import forms
from .models import SensorValue, AlertSensor


class CreateSensorValueForm(forms.ModelForm):
    class Meta:
        model = SensorValue
        fields = ['station', 'sensor_type',
                  'sensor_value', 'datetime_collected']


class CreateAlertSensorForm(forms.ModelForm):
    class Meta:
        model = AlertSensor
        fields = ['station', 'sensor_type', 'operator',
                  'main_value', 'second_value', 'time_frequency']
