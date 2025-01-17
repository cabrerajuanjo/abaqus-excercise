from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from portfolio.models import Asset, Portfolio, Date
import portfolio.selectors as selectors
from portfolio.services import extract_transform_load, transact, reset


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
    parser_classes = (MultiPartParser, FormParser,)

    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()
        initial_total = serializers.FloatField()

    def post(self, request: Request, format=None):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        my_file = request.FILES['file']

        data = extract_transform_load.execute(
            my_file, serializer.validated_data['initial_total']
        )
        return Response(data)


class PortfolioTransact(APIView):
    class InputSerializer(serializers.Serializer):
        date = serializers.DateField()
        portfolio = serializers.CharField(max_length=200)
        asset = serializers.CharField(max_length=200)
        operation = serializers.ChoiceField(choices=("BUY", "SELL"))
        amount = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = transact.execute(
            date=serializer.validated_data['date'],
            portfolio=serializer.validated_data['portfolio'],
            asset=serializer.validated_data['asset'],
            operation=serializer.validated_data['operation'],
            amount_delta=serializer.validated_data['amount']
        )

        return Response(data)


class PortfolioReset(APIView):
    def post(self, request: Request):
        reset.execute()

        return Response(status=200)


class PortfolioPortfolios(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Portfolio
            fields = ["name"]

        def to_representation(self, instance):
            return instance.name

    def get(self, request: Request):
        result = selectors.portfolios()
        print(result)

        return Response(self.OutputSerializer(result, many=True).data)


class PortfolioAssets(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Asset
            fields = ["name"]

        def to_representation(self, instance):
            return instance.name

    def get(self, request: Request):
        result = selectors.assets()

        return Response(self.OutputSerializer(result, many=True).data)

class PortfolioDates(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Date
            fields = ["date"]

        def to_representation(self, instance):
            return instance.date

    def get(self, request: Request):
        result = selectors.dates()

        return Response(self.OutputSerializer(result, many=True).data)
