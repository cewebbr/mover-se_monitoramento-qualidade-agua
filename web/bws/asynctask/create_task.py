import os
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bws.settings")
django.setup()


schedule, _ = CrontabSchedule.objects.get_or_create(every='10', period=IntervalSchedule.MINUTES)

PeriodicTask.objects.create(
        crontab=schedule,
        name='Importing contacts',
        task='bws.asynctask.tasks.check_alarms')

"""CrontabSchedule.objects.get_or_create(
        minute='3',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*')
"""
