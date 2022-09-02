from rest_framework import serializers
from station.models import SensorValue


class SensorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorValue
        fields = ['station', 'sensor_type', 'sensor_value',
                  'datetime_collected', 'from_api']
