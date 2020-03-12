import decimal

import requests

from currency_exchanger.models import ExchangeRate


class SomethingWentWrongException(Exception):
    pass


class UnexpectedBaseCurrencyException(Exception):
    pass


class ExchangeRateService(object):
    def __init__(self, *args, **kwargs):
        self.symbols = ['USD', 'CZK', 'PLN', 'EUR']
        super().__init__(*args, **kwargs)

    def convert(self, base, target, amount):
        try:
            instance = ExchangeRate.objects.get(base_currency=base, target_currency=target)
        except ExchangeRate.DoesNotExist:
            return None
        return decimal.Decimal(amount) * instance.rate

    def update_table(self):
        result = dict(
            created_objs_count=0,
            updated_objs_count=0
        )
        for base_currency in self.symbols:
            try:
                rates = self.get_rates_from_external_api(base_currency)
            except SomethingWentWrongException:
                continue
            for target_currency, rate in rates.items():
                obj, created = ExchangeRate.objects.update_or_create(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    defaults=dict(
                        base_currency=base_currency,
                        target_currency=target_currency,
                        rate=decimal.Decimal(rate).quantize(decimal.Decimal('1.00'))
                    )
                )

                if created:
                    result['created_objs_count'] += 1
                else:
                    result['updated_objs_count'] += 1

        return result

    def get_rates_from_external_api(self, base_currency):
        symbols = self.symbols.copy()

        try:
            symbols.remove(base_currency)
        except ValueError:
            raise UnexpectedBaseCurrencyException

        query_params = dict(
            base=base_currency,
            symbols=",".join(symbols)
        )

        response = requests.get('https://api.exchangeratesapi.io/latest', params=query_params)

        if response.status_code == 400:
            raise SomethingWentWrongException

        data = response.json()

        return data['rates']
