import rest_framework.generics as drf_spectacular
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.core.models import Status
from sngf_api.plant.models import Plant
from sngf_api.plant.models import Seed

from .serializers import PlantSerializer
from .serializers import SeedSerializer


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


class GetListPlantView(drf_spectacular.ListAPIView):
    queryset = Plant.objects.all().filter(status=Status.STATUS.ACTIVE)
    serializer_class = PlantSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        category = self.request.query_params.get("category")
        size = self.request.query_params.get("size")
        status_param = self.request.query_params.get("status")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if size:
            queryset = queryset.filter(plant_size_price__size=size)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset.distinct()


class GetPlantByIdView(drf_spectacular.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class GetListSeedView(drf_spectacular.ListAPIView):
    queryset = Seed.objects.all().filter(status=Status.STATUS.ACTIVE)
    serializer_class = SeedSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        category = self.request.query_params.get("category")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)

        return queryset.distinct()


class GetSeedByIdView(drf_spectacular.RetrieveAPIView):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
