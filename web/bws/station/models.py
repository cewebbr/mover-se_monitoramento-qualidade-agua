from django.db import models
from django.contrib.auth.models import User


class StationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    key = models.CharField(max_length=50, unique=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Station(models.Model):
    identification = models.CharField(max_length=50, unique=True)
    station_type = models.ForeignKey(
        StationType, on_delete=models.SET_NULL, null=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1024)
    latitude = models.DecimalField(
        max_digits=18, decimal_places=15, default=None)
    longitude = models.DecimalField(
        max_digits=18, decimal_places=15, default=None)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.identification}"


class Sensor(models.Model):
    GRAPH_CHOICE = (
        (1, 'Percentage'),
        (2, 'Thermometer'),
        (3, 'Number'),
    )

    key = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100, unique=True)
    graphic_type = models.IntegerField(default=1, choices=GRAPH_CHOICE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class SensorStation(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    sensor_type = models.ForeignKey(
        Sensor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.station} - {self.sensor_type}"


class SensorValue(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    sensor_type = models.ForeignKey(
        Sensor, on_delete=models.SET_NULL, null=True)
    sensor_value = models.CharField(max_length=30)
    datetime_collected = models.DateTimeField()
    datetime_creation = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    # sent from api (arduino station)
    from_api = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.station} - {self.sensor_type}: {self.sensor_value}"

    class Meta:
        ordering = ("-datetime_creation",)


class AlertSensor(models.Model):
    ENTRE_OPERATOR = "Entre"
    IGUAL_OPERATOR = "Igual"
    MAIOR_OPERATOR = "Maior"
    MENOR_OPERATOR = "Menor"

    DURATION_CHOICE = (
        ("60", '1 hora'),
        ("180", '3 horas'),
        ("300", '5 horas'),
        ("600", '10 horas'),
    #   ("3", '3 Minutos') #test only
    )

    OPERATOR_CHOICES = (
        (ENTRE_OPERATOR, 'Entre'),
        (IGUAL_OPERATOR, 'igual'),
        (MAIOR_OPERATOR, 'maior'),
        (MENOR_OPERATOR, 'menor')
    )

    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    sensor_type = models.ForeignKey(
        Sensor, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    operator = models.CharField(
        max_length=10, choices=OPERATOR_CHOICES,  null=True)
    main_value = models.CharField(max_length=3, null=False)
    second_value = models.CharField(max_length=3, null=True, blank=True)
    time_frequency = models.CharField(
        max_length=5, choices=DURATION_CHOICE, null=False)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    prev_exec = models.DateTimeField('Última execução', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.station} - {self.sensor_type} : {self.time_frequency}"

    class Meta:
        ordering = ("-datetime_creation",)
