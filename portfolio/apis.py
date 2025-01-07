# from django.shortcuts import Http404
# from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers

# from styleguide_example.api.pagination import (
#     LimitOffsetPagination,
#     get_paginated_response,
# )
from portfolio.services import extract_transform_load

# TODO: When JWT is resolved, add authenticated version


class PortfolioData(APIView):
    # class OutputSerializer(serializers.Serializer):
    #     id = serializers.IntegerField()
    #     email = serializers.CharField()
    class InputSerializer(serializers.Serializer):
        from_date = serializers.DateField(required=False)
        to_date = serializers.DateField(required=False)

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # data = extract_transform_load.execute()

        # return Response(data)

    def post(self, request: Request):
        data = extract_transform_load.execute()
        return Response(data)
