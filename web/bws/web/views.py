from django.core.mail import send_mail
from bws.settings import EMAIL_FAIL_SILENT, DEFAULT_FROM_EMAIL
from watersource.models import WaterSource
from station.models import AlertSensor, Station
from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
logger = logging.getLogger(__name__)


def index(request):

    return render(request, 'web/index.html')


def map(request):

    pointers_station = Station.objects.all()
    pointers_springs_water = WaterSource.objects.all()

    stations = list()
    springs_water = list()

    for station in pointers_station:
        stations.append({
            'id': station.id,
            'titulo': station.identification,
            'lat': station.latitude,
            'lon': station.longitude,
            'custom_icon': 'water_quality.png',
            'url': 'station/'
        })

    for spring_water in pointers_springs_water:
        springs_water.append({
            'id': spring_water.id,
            'titulo': spring_water.identification,
            'lat': spring_water.latitude,
            'lon': spring_water.longitude,
            'custom_icon': 'springwater.png',
            'url': 'spring-water/view/'
        })

    return JsonResponse({'map': [stations, springs_water]}, safe=False)


def searchPointer(request):

    search = request.GET.get('station')

    if request.is_ajax():

        station = Station.objects.filter(identification__icontains=search)
        spring_water = WaterSource.objects.filter(
            identification__icontains=search)

        searchPointers = list()

        for i in range(len(station)):
            searchPointers.append({'id': station[i].id, 'name': station[i].identification,
                                  'description': station[i].station_type.name, 'path': 'station/'})

        for i in range(len(spring_water)):
            searchPointers.append({'id': spring_water[i].id, 'name': spring_water[i].identification,
                                  'description': spring_water[i].description, 'path': 'spring-water/view/'})

        return JsonResponse({'point': searchPointers}, status=200)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('web:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('web:index')
        else:
            messages.info(request, 'Verificar nome de usuário ou senha')

    context = {}
    return render(request, 'registration/login.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('web:login')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Usuário criado para ' +
                             user + '. Aguardar liberação do administrador.')

            body = f'Usuário {user} cadastrado no sistema.\n \
            Acesse ao painel de administração para liberar o acesso.'
            subject = 'Liberação de acesso de usuário'

            user = User.objects.filter(is_superuser=True)
            for super_user in user:
                try:
                    send_mail(subject, body, DEFAULT_FROM_EMAIL, [
                            super_user.email], fail_silently=EMAIL_FAIL_SILENT)
                except:
                    print(f"Falha no envio de alerta de criação do usuário para {super_user.email}")

            return redirect('web:login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def perfil(request, id):

    user = User.objects.get(id=id)
    alert = len(AlertSensor.objects.filter(user=user))
    # Deixar o objeto para ser exibido o link de todas as nascentes num futuro.
    watersources = WaterSource.objects.filter(user=user)
    return render(request, 'web/perfil.html', {'user': user, 'countAlert': alert, 'watersources': watersources})


def about(request):
    return render(request, 'web/about.html', {})
