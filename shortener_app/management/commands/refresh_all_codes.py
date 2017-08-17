from django.core.management.base import BaseCommand, CommandError
from shortener_app.models import WinURL


class Command(BaseCommand):
    help = 'Refresh all WinURL shortcodes'


    def add_arguments(self, parser):
        parser.add_argument('-items', type=int)


    def handle(self, *args, **options):
        return WinURL.objects.refresh_all_shortcodes(options['items'])