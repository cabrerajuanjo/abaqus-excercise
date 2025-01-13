from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
import portfolio.selectors as selectors
from portfolio.services import extract_transform_load


class PortfolioWeight(APIView):
    class InputSerializer(serializers.Serializer):
        page = serializers.IntegerField(required=False)
        perPage = serializers.IntegerField(required=False)
        date__lt = serializers.DateField(required=False)
        date__gt = serializers.DateField(required=False)

    class OutputSerializer(serializers.Serializer):
        date = serializers.DateField()
        asset = serializers.CharField(max_length=200)
        portfolio = serializers.CharField(max_length=200)
        weight = serializers.FloatField()

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = selectors.getWeights(filters=serializer.validated_data)

        return Response(self.OutputSerializer(result, many=True).data)


class PortfolioTotal(APIView):
    class InputSerializer(serializers.Serializer):
        date__lt = serializers.DateField(required=False)
        date__gt = serializers.DateField(required=False)

    class OutputSerializer(serializers.Serializer):
        date = serializers.DateField()
        portfolio = serializers.CharField(max_length=200)
        total_amount = serializers.FloatField()

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        result = selectors.getTotals(filters=serializer.validated_data)

        return Response(self.OutputSerializer(result, many=True).data)


class PortfolioLoadData(APIView):
    def post(self, request: Request):
        data = extract_transform_load.execute()
        return Response(data)
