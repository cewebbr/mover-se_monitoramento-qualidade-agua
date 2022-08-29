from bws.settings import EMAIL_FAIL_SILENT, EMAIL_HOST_USER
from celery import shared_task
from django.utils import timezone
from station.models import AlertSensor, SensorValue
from sys import stdout
from datetime import timedelta
from django.db.models import Q
from django.core.mail import send_mail


@shared_task
def exec_alert(alert_id):
    """
    Task responsável por checar os dados de um alerta. Ela recebe o id do alerta e checa se houve alguma informação
    que deve ser reportada para o usuário.
    """
    stdout.write("Iniciando execução...\n")
    alert = AlertSensor.objects.get(pk=alert_id)
    stdout.write(f"{alert}\n")

    if alert.prev_exec:
        filter_date = alert.prev_exec
    else:
        filter_date = alert.datetime_creation

    stdout.write(f"Checando envios a partir de {filter_date}...\n")
    filter_options = Q(station=alert.station, sensor_type=alert.sensor_type,
                       datetime_creation__gte=filter_date)

    if alert.operator == AlertSensor.ENTRE_OPERATOR:
        filter_options.add(Q(sensor_value__gte=alert.main_value), Q.AND)
        filter_options.add(Q(sensor_value__lte=alert.second_value), Q.AND)
    elif alert.operator == AlertSensor.IGUAL_OPERATOR:
        filter_options.add(Q(sensor_value=alert.main_value), Q.AND)
    elif alert.operator == AlertSensor.MAIOR_OPERATOR:
        filter_options.add(Q(sensor_value__gte=alert.main_value), Q.AND)
    elif alert.operator == AlertSensor.MENOR_OPERATOR:
        filter_options.add(Q(sensor_value__lte=alert.main_value), Q.AND)

    data_filtered = SensorValue.objects.filter(filter_options)

    if data_filtered:
        body = f"Olá!\nEste é um email de alerta do sensor {alert.sensor_type.name}\n"
        for sensor_value in data_filtered:
            body += f"Valor do sensor {sensor_value.sensor_value} às {sensor_value.datetime_collected}\n"

        body += "\n\n### E-mail automático. Não responda. ###"

        if alert.user.email:
            stdout.write("Enviando e-mail...\n")
            subject = f"Alerta do sensor {alert.sensor_type.name} da estação  {alert.station}"

            send_mail(subject, body, EMAIL_HOST_USER, [
                      alert.user.email], fail_silently=EMAIL_FAIL_SILENT)
            stdout.write(f"E-mail enviado às {alert.prev_exec}...\n")
        else:
            stdout.write(
                f"Error! {alert.user.username}' não possui e-mail definido.\n")

    alert.prev_exec = timezone.now()
    alert.save()


@shared_task
def cron_read_alerts():
    """
    Task responsável por pegar todos os alertas e executar aqueles que precisem ser executados
    Para esta task rodar é necessário criar uma Periodic Task no painel de administração do Django.
    """
    stdout.write("Lendos os alertas\n")
    now = timezone.now()
    alerts = AlertSensor.objects.all()
    for alert in alerts:
        prev_exec = alert.prev_exec
        stdout.write(str(alert) + '\n')

        if prev_exec:
            next_exec = prev_exec + \
                timedelta(minutes=int(alert.time_frequency))
        else:
            next_exec = now

        if now >= next_exec:
            stdout.write(f"Start execution {alert.pk}\n")
            exec_alert.delay(alert.pk)
