from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from . import APIParser


@api_view(['POST'])
def postSensorValue(request):
    if request.method == "POST":
        station_data = JSONParser().parse(request)

        version = station_data["version"]
        if version == APIParser.Version1Parser.VERSION:
            parser = APIParser.Version1Parser(station_data)
            response = parser.parse_req()
        else:
            return JsonResponse({APIParser.MESSAGE_KEY: f"Versão da API \
                                 inválida (versão={version})"},
                                status=status.HTTP_400_BAD_REQUEST)
        return response
