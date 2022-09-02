from django.core.management.base import BaseCommand
from asynctask.tasks import exec_alert


class Command(BaseCommand):

    help = 'Run alert by PK'

    def handle(self, *args, **options):
        for alert_id in options['alert_id']:
            self.stdout.write(f"{alert_id}\n")
            exec_alert.delay(alert_id)
            self.stdout.write(self.style.SUCCESS('Successfully executed alert "%s"\n' % alert_id))

    def add_arguments(self, parser):
        parser.add_argument('alert_id', nargs='+', type=int)
