# from django.shortcuts import Http404
# from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get(self, request):
        extract_transform_load.execute()

        # data = self.OutputSerializer(data).data

        return Response("data")
