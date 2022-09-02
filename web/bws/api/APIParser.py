from station.models import SensorStation, Station
from django.http.response import JsonResponse
from rest_framework import status
from .serializers import SensorValueSerializer

# Constantes
MESSAGE_KEY = "resposta"
STATUS_KEY = "sensor_status"
SAVE_SUCC = "ok"


class APIParser():
    def __init__(self, version):
        self.version = version

    def parse_req(self):
        raise NotImplementedError()


class Version1Parser(APIParser):
    VERSION = 1

    def __init__(self, station_data):
        super().__init__(Version1Parser.VERSION)
        self.station_data = station_data

    def parse_req(self):
        try:
            base_id = self.station_data["base_id"]
            station = Station.objects.get(identification=base_id)
        except Station.DoesNotExist:
            return JsonResponse({MESSAGE_KEY: f"Estação {base_id} não existe na base."},
                                status=status.HTTP_400_BAD_REQUEST)  # https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

        sensors_items = self.station_data["sensors"].items()
        datetime_collected = self.station_data["datetime"]
        out_messages = {}

        for sensor_key, sensor_value in sensors_items:
            if SensorStation.objects.filter(sensor_type__key=sensor_key, station=station).exists():
                out_messages[sensor_key] = self.__save_sensor_data(
                    station.id, sensor_key, sensor_value, datetime_collected)
            else:
                out_messages[sensor_key] = f"Sensor {sensor_key} não existe na estação {base_id}."

        if SAVE_SUCC in out_messages.values():
            response_status = status.HTTP_201_CREATED
            size_ok = list(out_messages.values()).count(SAVE_SUCC)

            if size_ok == len(out_messages):
                message = "Todos os sensores foram adicionados com sucesso."
            else:
                message = f"{size_ok} sensor(s) adicionado(s).\
{len(out_messages) - size_ok} sensor(es) não adicionado(s)."
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            message = "Nenhum sensor foi adicionado com sucesso."

        response = {MESSAGE_KEY: message,
                    STATUS_KEY: out_messages}

        return JsonResponse(response, status=response_status)

    def __save_sensor_data(self, station, sensor_key, sensor_value, datetime_collected):
        sensor_data = self.__create_sensor_data(
            station, sensor_key, sensor_value, datetime_collected)
        sensor_data_serializer = SensorValueSerializer(data=sensor_data)
        if sensor_data_serializer.is_valid():
            sensor_data_serializer.save()
            out_message = SAVE_SUCC
        else:
            out_message = sensor_data_serializer.errors
        return out_message

    def __create_sensor_data(self, station, sensor_type, sensor_value,
                             datetime_collected, from_api=True):
        data = {
            "station": station,
            "sensor_type": sensor_type,
            "sensor_value": sensor_value,
            "datetime_collected": datetime_collected,
            "from_api": from_api,
        }
        return data
