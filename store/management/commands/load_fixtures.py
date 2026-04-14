from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Загружает начальные данные из фикстуры'

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data.json')
        self.stdout.write(self.style.SUCCESS('Фикстуры успешно загружены'))