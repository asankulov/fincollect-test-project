from django.db import models


class ExchangeRate(models.Model):
    base_currency = models.CharField(verbose_name='Base Currency', max_length=3)
    target_currency = models.CharField(verbose_name='Target Currency', max_length=3)
    rate = models.DecimalField(verbose_name='Rate', max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'Exchange Rate'
        verbose_name_plural = 'Exchange Rates'
        constraints = [
            models.UniqueConstraint(fields=['base_currency', 'target_currency'], name='unique_currency_pair')
        ]

    def save(self, *args, **kwargs):
        self.base_currency = self.base_currency.upper()
        self.target_currency = self.target_currency.upper()
        super().save(*args, **kwargs)

