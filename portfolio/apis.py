from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from portfolio.models.models import Weight, Amount

from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from portfolio.services import extract_transform_load, weight

# TODO: When JWT is resolved, add authenticated version


class PortfolioData(APIView):
    # class OutputSerializer(serializers.Serializer):
    #     id = serializers.IntegerField()
    #     email = serializers.portcwwolio.apiCharField()

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSerializer(serializers.Serializer):
        date__lt = serializers.DateField(required=False)
        date__gt = serializers.DateField(required=False)

    class OutputSerializerAmount(serializers.ModelSerializer):
        class Meta:
            model = Amount
            fields = ("date", "amount", "portfolio", "asset")

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Weight
            fields = ("date", "asset", "portfolio", "weight")

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        result = weight.get(filters=serializer.validated_data)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializerAmount,
            queryset=result,
            request=request,
            view=self,
        )

        return Response(result)

    def post(self, request: Request):
        data = extract_transform_load.execute()
        # print (data)
        return Response(data)
