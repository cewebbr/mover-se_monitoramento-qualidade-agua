import datetime
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Station, SensorStation, SensorValue, AlertSensor
import logging
from .forms import CreateAlertSensorForm, CreateSensorValueForm
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404

logger = logging.getLogger(__name__)

# Create your views here.


def stationDetail(request, id):
    pointer_station = get_object_or_404(Station, pk=id)

    sensors_types = SensorStation.objects.filter(
        station__pk=int(id)).values('sensor_type__key')

    data = {}
    graphic = []

    for data_sensor in sensors_types:
        sensor_type = data_sensor['sensor_type__key']
        queryset = SensorValue.objects.filter(
            station_id=pointer_station.id, sensor_type__key=sensor_type)
        if queryset:
            sensor = queryset.latest('datetime_collected')
            dict_obj = model_to_dict(sensor)
            data[sensor_type] = dict_obj
            data[sensor_type]['sensor_type_name'] = sensor.sensor_type.name
            graphic.append(sensor)

    return render(request, 'station/stationDetails.html', {'pointer_station': pointer_station, 'sensors': data, 'graphic': graphic})


def sensorDetail(request, id_station, id_sensor):

    station = get_object_or_404(Station, pk=id_station)
    sensor_station = SensorStation.objects.filter(
        station=id_station, sensor_type=id_sensor).first()
    if not sensor_station:
        raise Http404(
            f"Sensor {id_sensor} not found in {station.identification}.")
    sensor = sensor_station.sensor_type

    sensorList = []
    valueList = []
    monthCurrent = datetime.datetime.now().month

    monthName = ''
    firstDate = ''
    lastDate = ''

    month = request.GET.get('month')
    dayBegin = request.GET.get('begin')
    dayEnd = request.GET.get('end')

    if month and month.isdigit():
        monthCurrent = int(month)

    if dayBegin and dayEnd:
        firstDate = datetime.date(int(dayBegin[:4]), int(
            dayBegin[5:7]), int(dayBegin[8:]))
        lastDate = datetime.date(
            int(dayEnd[:4]), int(dayEnd[5:7]), int(dayEnd[8:]))

    monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    if monthCurrent == datetime.datetime.now().month:
        monthName = 'Mês Atual'
    else:
        monthName = monthNames[monthCurrent-1]

    if firstDate and lastDate:
        filteredData = SensorValue.objects.filter(sensor_type=sensor.key, station_id=station.id, datetime_collected__range=(
            firstDate, lastDate)).order_by('datetime_collected')
    else:
        filteredData = SensorValue.objects.filter(sensor_type=sensor.key, station_id=station.id, datetime_collected__month=monthCurrent,
                                                  datetime_collected__year=datetime.datetime.now().year).order_by('datetime_collected')

    for sensorData in filteredData:
        sensorList.append(float(sensorData.sensor_value))
        dateFormated = sensorData.datetime_collected.strftime(
            '%d/%m/%Y - %H:%M:%S')
        valueList.append(
            {'date': dateFormated, 'value': sensorData.sensor_value, })

    valueList.reverse()

    sensorCurrent = SensorValue.objects.filter(
        sensor_type=sensor.key, station_id=station.id).latest('datetime_collected')
    return render(request, 'station/sensorDetail.html', {'sensorCurrent': sensorCurrent, 'sensors': sensorList, 'data': valueList, 'month': monthName})


def sensorValuesAjax(request, id):

    sensor = request.GET.get('sensor')

    if request.is_ajax():
        sensor = SensorValue.objects.filter(
            sensor_type=sensor, station=id).latest('datetime_collected')
        sensorValues = list()
        sensorValues.append({'value': sensor.sensor_value,
                            'datetime': sensor.datetime_collected})

        return JsonResponse({'sensor': sensorValues})


def newSensorValue(request):

    station = Station.objects.all()
    form = CreateSensorValueForm()

    if request.method == 'POST':
        form = CreateSensorValueForm(request.POST)

        if form.is_valid():
            valueSensor = form.save()
            valueSensor.datetime_creation = timezone.now()
            valueSensor.save()
            messages.success(request, 'Valor cadastrado com sucesso!')

        else:
            messages.info(request, 'Erro ao inserir valores!')

    return render(request, 'station/newSensorValue.html', {'stations': station, 'form': form})


@login_required
def alert(request):

    stations = Station.objects.all()
    form = CreateAlertSensorForm()

    if request.method == 'POST':
        form = CreateAlertSensorForm(request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                alert = form.save()
                alert.datetime_creation = datetime.datetime.now()
                alert.user = request.user
                alert.prev_exev = None
                alert.save()
                messages.success(request, 'alerta cadastrado com sucesso')
                return redirect('station:alert')

            else:
                messages.info(request, 'Erro ao inserir valores!')

    alerts = AlertSensor.objects.filter(
        user=request.user).order_by('datetime_creation')
    time = dict(AlertSensor.DURATION_CHOICE)
    operator = dict(AlertSensor.OPERATOR_CHOICES)

    return render(request, 'station/alert.html', {'alerts': alerts, 'stations': stations, 'time': time, 'operator': operator, 'form': form})


def sensorAjax(request):

    station = request.GET.get('station')
    if request.is_ajax():
        sensores_queryset = SensorStation.objects.filter(
            station__pk=int(station))
        sensors = {sensor_type_station.sensor_type.key:
                   sensor_type_station.sensor_type.name for sensor_type_station in sensores_queryset}
        return JsonResponse({'sensores': sensors}, status=200)


def deleteAlert(request, id):
    alert = get_object_or_404(AlertSensor, pk=id)

    if request.method == 'POST':
        alert.delete()
        return redirect('station:alert')

    return render(request, 'station:alert', {})
