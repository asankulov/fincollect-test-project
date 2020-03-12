from rest_framework import serializers


currency_choices = [
    ('EUR', 'eur'),
    ('USD', 'usd'),
    ('PLN', 'pln'),
    ('CZK', 'czk')
]


class CurrencyConvertSerializer(serializers.Serializer):
    base = serializers.ChoiceField(choices=currency_choices)
    target = serializers.ChoiceField(choices=currency_choices)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
