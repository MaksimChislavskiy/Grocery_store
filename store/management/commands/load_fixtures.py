from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Загружает начальные данные из фикстуры'

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data.json')
        self.stdout.write(self.style.SUCCESS('Фикстуры успешно загружены'))