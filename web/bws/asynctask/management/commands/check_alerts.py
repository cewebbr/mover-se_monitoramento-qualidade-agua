from django.core.management.base import BaseCommand
from asynctask.tasks import cron_read_alerts


class Command(BaseCommand):

    help = 'Check alerts that needs to be processed'

    def handle(self, *args, **options):
        cron_read_alerts()
