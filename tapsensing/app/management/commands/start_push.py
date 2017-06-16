from django.core.management.base import BaseCommand

from ...tasks.pushnotifications import send_push_notifications


class Command(BaseCommand):
    help = 'Starts the push notifications.'

    def handle(self, *args, **options):
        send_push_notifications()
