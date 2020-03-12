from io import StringIO
from unittest import mock

from django.test import TestCase
from django.core.management import call_command


class ManagementCommandTestCase(TestCase):
    @mock.patch('currency_exchanger.services.ExchangeRateService.update_table')
    def test_renew_table_command(self, mock_update_table):
        update_table_return_value = dict(
            created_objs_count=3,
            updated_objs_count=4
        )
        mock_update_table.return_value = update_table_return_value
        out = StringIO()
        call_command('renew_table', stdout=out)
        self.assertEqual(mock_update_table.call_count, 1)
        self.assertIn('updated', out.getvalue())
        self.assertIn('created', out.getvalue())
        self.assertIn(str(update_table_return_value['created_objs_count']), out.getvalue())
        self.assertIn(str(update_table_return_value['updated_objs_count']), out.getvalue())
