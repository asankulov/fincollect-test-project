import decimal
from random import uniform
from unittest import mock
from unittest.mock import PropertyMock

from rest_framework.test import APITestCase


class ExchangeAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.valid_base_query_param = 'USD'
        self.valid_target_query_param = 'EUR'
        self.valid_amount_query_param = decimal.Decimal(uniform(0.5, 10000.05))
        self.valid_serializer_data = {
            'base': self.valid_base_query_param,
            'target': self.valid_target_query_param,
            'amount': self.valid_amount_query_param
        }

    @mock.patch('currency_exchanger.services.ExchangeRateService.convert')
    @mock.patch('currency_exchanger.serializers.CurrencyConvertSerializer.data',
                new_callable=PropertyMock)
    @mock.patch('currency_exchanger.serializers.CurrencyConvertSerializer.is_valid', return_value=True)
    def test_currency_convert_success(self, mock_is_valid, mock_data, mock_convert):
        mock_data.return_value = self.valid_serializer_data
        mock_convert.return_value = decimal.Decimal(uniform(0.5, 10000.05))

        response = self.client.get(f"/api/exchange/?"
                                   f"base={self.valid_base_query_param}&"
                                   f"target={self.valid_target_query_param}&"
                                   f"amount={self.valid_amount_query_param}")

        self.assertEqual(mock_data.call_count, 1)
        self.assertEqual(mock_is_valid.call_count, 1)
        self.assertEqual(mock_convert.call_count, 1)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {'result': mock_convert.return_value})

    @mock.patch('currency_exchanger.serializers.CurrencyConvertSerializer.is_valid', return_value=True)
    @mock.patch('currency_exchanger.serializers.CurrencyConvertSerializer.data',
                new_callable=PropertyMock)
    @mock.patch('currency_exchanger.services.ExchangeRateService.convert', return_value=None)
    def test_currency_convert_currency_not_found(self, mock_is_valid, mock_data, mock_convert):
        mock_data.return_value = self.valid_serializer_data
        mock_convert.return_value = None

        response = self.client.get(f"/api/exchange/?"
                                   f"base={self.valid_base_query_param}&"
                                   f"target={self.valid_target_query_param}&"
                                   f"amount={self.valid_amount_query_param}")

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, {'message': 'Selecting currencies exchange rate data not found'})

