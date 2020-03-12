from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CurrencyConvertSerializer
from .services import ExchangeRateService


class CurrencyConvertAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CurrencyConvertSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        exchange_service = ExchangeRateService()
        result = exchange_service.convert(**validated_data)

        if result is None:
            return Response({'message': 'Selecting currencies exchange rate data not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'result': result}, status=status.HTTP_200_OK)



