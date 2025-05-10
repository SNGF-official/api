from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.core.models import Status
from sngf_api.plant.models import Plant
from sngf_api.plant.models import Seed

from .mixins import FilterQueryMixin
from .serializers import PlantSerializer
from .serializers import SeedSerializer


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


class GetListSeedView(FilterQueryMixin, ListAPIView):
    queryset = Seed.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = SeedSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset_by_params(queryset, self.request.query_params)


class GetSeedByIdView(RetrieveAPIView):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class GetListPlantView(FilterQueryMixin, ListAPIView):
    queryset = Plant.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = PlantSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        extra_filters = {}

        return self.filter_queryset_by_params(queryset, params, extra_filters)


class GetPlantByIdView(RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class CreateSeedView(CreateAPIView):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = [AllowAny]


class UpdateSeedView(UpdateAPIView):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class CreatePlantView(CreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]


class UpdatePlantView(UpdateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
