from django.urls import path

from currency_exchanger.views import CurrencyConvertAPIView

urlpatterns = [
    path('exchange/', CurrencyConvertAPIView.as_view(), name='exchange')
]