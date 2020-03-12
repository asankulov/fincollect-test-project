from django.core.management.base import BaseCommand

from currency_exchanger.services import ExchangeRateService


class Command(BaseCommand):

    help = 'Renew exchange rate table'

    def handle(self, *args, **options):
        exchange_service = ExchangeRateService()
        result = exchange_service.update_table()
        self.stdout.write(self.style.SUCCESS(f'Results: \n'
                                             f'updated: {result["updated_objs_count"]}\n'
                                             f'created: {result["created_objs_count"]}'))

    def execute(self, *args, **options):
        super().execute(*args, **options)
        return 0
