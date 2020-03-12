import decimal
import itertools
from random import uniform
from unittest import mock

from django.test import TransactionTestCase

from currency_exchanger.services import ExchangeRateService, SomethingWentWrongException, \
    UnexpectedBaseCurrencyException
from tests.factories import ExchangeRateFactory, ExternalAPIResponseFactory


class ExchangeServiceTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.exchange_rate_service = ExchangeRateService()
        self.external_api_response_factory = ExternalAPIResponseFactory()
        self.mock_get_patcher = mock.patch('requests.get')
        self.mock_get = self.mock_get_patcher.start()

    def tearDown(self) -> None:
        self.mock_get_patcher.stop()

    def test_get_rates_from_external_api_with_valid_currency(self):
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = self.external_api_response_factory.response_dict

        self.assertDictEqual(self.external_api_response_factory.response_dict['rates'],
                             self.exchange_rate_service.get_rates_from_external_api('USD'))
        self.assertTrue(self.mock_get.called)
        self.assertTrue(self.mock_get.call_count, 1)
        self.assertDictEqual(self.mock_get.call_args[-1], dict(
            params=dict(
                base='USD',
                symbols='CZK,PLN,EUR'
            )
        ))

    def test_get_rates_from_external_api_with_invalid_currency(self):
        with self.assertRaises(UnexpectedBaseCurrencyException):
            self.exchange_rate_service.get_rates_from_external_api('KGS')
        self.assertFalse(self.mock_get.called)

    def test_get_rates_from_external_api_when_bad_status_from_api(self):
        self.mock_get.return_value.status_code = 400
        with self.assertRaises(SomethingWentWrongException):
            self.exchange_rate_service.get_rates_from_external_api('PLN')

    @mock.patch('currency_exchanger.models.ExchangeRate.objects.update_or_create')
    @mock.patch('currency_exchanger.services.ExchangeRateService.get_rates_from_external_api')
    def test_update_table_only_updates(self, mock_get_rates_from_external_api, mock_update_or_create):
        mock_get_rates_from_external_api.return_value = self.external_api_response_factory.rates
        mock_update_or_create.return_value = ExchangeRateFactory(), False

        result = self.exchange_rate_service.update_table()

        self.assertIn('created_objs_count', result)
        self.assertIn('updated_objs_count', result)
        self.assertNotEqual(result['created_objs_count'], result['updated_objs_count'])
        self.assertEqual(mock_update_or_create.call_count, result['created_objs_count'] + result['updated_objs_count'])
        self.assertTrue(mock_get_rates_from_external_api.called)

    @mock.patch('currency_exchanger.models.ExchangeRate.objects.update_or_create')
    @mock.patch('currency_exchanger.services.ExchangeRateService.get_rates_from_external_api')
    def test_update_table_with_exceptions(self, mock_get_rates_from_external_api, mock_update_or_create):
        mock_get_rates_from_external_api.side_effect = SomethingWentWrongException()
        mock_update_or_create.return_value = ExchangeRateFactory(), False

        result = self.exchange_rate_service.update_table()

        self.assertEqual(result['created_objs_count'], 0)
        self.assertEqual(result['updated_objs_count'], 0)
        self.assertFalse(mock_update_or_create.called)

    @mock.patch('currency_exchanger.models.ExchangeRate.objects.update_or_create')
    @mock.patch('currency_exchanger.services.ExchangeRateService.get_rates_from_external_api')
    def test_update_table_with_creates_and_updates(self, mock_get_rates_from_external_api, mock_update_or_create):
        mock_get_rates_from_external_api.return_value = self.external_api_response_factory.rates
        mock_update_or_create.side_effect = itertools.cycle([
            (ExchangeRateFactory(), False),
            (ExchangeRateFactory(), True)
        ])

        result = self.exchange_rate_service.update_table()

        self.assertEqual(result['created_objs_count'], result['updated_objs_count'])
        self.assertTrue(mock_get_rates_from_external_api.called)

    def test_convert_with_existing_currencies(self):
        exchange_rate_factory_obj = ExchangeRateFactory()
        random_amount = decimal.Decimal(uniform(0.5, 10000.05))

        self.assertIsInstance(self.exchange_rate_service.convert(exchange_rate_factory_obj.base_currency,
                                                                 exchange_rate_factory_obj.target_currency,
                                                                 random_amount), decimal.Decimal)

    def test_convert_with_not_existing_currencies(self):
        exchange_rate_factory_obj_1 = ExchangeRateFactory()
        exchange_rate_factory_obj_2 = ExchangeRateFactory()
        random_amount = decimal.Decimal(uniform(0.5, 10000.05))

        self.assertIsNone(self.exchange_rate_service.convert(exchange_rate_factory_obj_1.base_currency,
                                                             exchange_rate_factory_obj_2.target_currency,
                                                             random_amount), decimal.Decimal)
