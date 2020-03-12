from rest_framework.test import APISimpleTestCase


from currency_exchanger.serializers import CurrencyConvertSerializer


class MyTestCase(APISimpleTestCase):
    def setUp(self) -> None:
        self.valid_serializable_data = {'base': 'USD', 'target': 'CZK', 'amount': 43.65}
        self.missed_one_field_serializable_data = {'base': 'USD', 'amount': 123.89}
        self.invalid_amount_field_serializable_data = {'base': 'EUR', 'target': 'PLN', 'amount': True}
        self.invalid_base_field_serializable_data = {'base': 'DRF', 'target': 'PLN', 'amount': 12.123}
        self.invalid_target_field_serializable_data = {'base': 'CZK', 'target': '3v53f', 'amount': 54.3}

    def test_with_valid_data(self):
        serializer = CurrencyConvertSerializer(data=self.valid_serializable_data)
        self.assertTrue(serializer.is_valid())

    def test_with_invalid_data(self):
        serializer = CurrencyConvertSerializer(data=self.missed_one_field_serializable_data)
        serializer.is_valid()

        serializer = CurrencyConvertSerializer(data=self.invalid_amount_field_serializable_data)
        self.assertFalse(serializer.is_valid())

        serializer = CurrencyConvertSerializer(data=self.invalid_base_field_serializable_data)
        self.assertFalse(serializer.is_valid())

        serializer = CurrencyConvertSerializer(data=self.invalid_target_field_serializable_data)
        self.assertFalse(serializer.is_valid())

