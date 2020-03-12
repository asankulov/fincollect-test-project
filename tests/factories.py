import datetime
from random import uniform

import factory

from currency_exchanger.models import ExchangeRate


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    base_currency = factory.Iterator(['EUR', 'USD', 'PLN', 'CZK'])
    target_currency = factory.Iterator(['PLN', 'EUR', 'CZK', 'USD'])
    rate = factory.LazyFunction(lambda: uniform(0.5, 100.05))

    class Meta:
        model = ExchangeRate


class ExternalAPIResponseFactory:
    rates = {
        'CZK': uniform(0.5, 100.05),
        'EUR': uniform(0.5, 100.05),
        'PLN': uniform(0.5, 100.05)
    }
    base = 'USD'
    date = datetime.datetime.now().strftime('%Y-%m-%d')

    @property
    def response_dict(self):
        return dict(
            rates=self.rates,
            base=self.base,
            date=self.date
        )

