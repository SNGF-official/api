from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response

from sngf_api.core.models import Status
from sngf_api.plant.models import Plant, Seed
from .serializers import PlantSerializer, SeedSerializer
from .filters import PlantFilter, SeedFilter


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


@extend_schema(
    parameters=[
        OpenApiParameter("name", str, description="Nom de la plante"),
        OpenApiParameter("keyword", str, description="Recherche par nom ou description"),
        OpenApiParameter("categories", str, description="Catégorie (code exact)"),
        OpenApiParameter("size", str, description="Taille (PM/MM/GM/EX/UN)"),
        OpenApiParameter("minQuantity", int),
        OpenApiParameter("maxQuantity", int),
        OpenApiParameter("minPrice", float),
        OpenApiParameter("maxPrice", float),
        OpenApiParameter("page", int),
        OpenApiParameter("pageSize", int),
    ]
)
class GetListPlantView(ListAPIView):
    queryset = Plant.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = PlantSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlantFilter


class GetPlantByIdView(RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
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


@extend_schema(
    parameters=[
        OpenApiParameter("name", str, description="Nom de la graine"),
        OpenApiParameter("keyword", str, description="Recherche par nom ou description"),
        OpenApiParameter("categories", str, description="Catégorie (code exact)"),
        OpenApiParameter("minQuantity", int),
        OpenApiParameter("maxQuantity", int),
        OpenApiParameter("minPrice", float),
        OpenApiParameter("maxPrice", float),
        OpenApiParameter("page", int),
        OpenApiParameter("pageSize", int),
    ]
)
class GetListSeedView(ListAPIView):
    queryset = Seed.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = SeedSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SeedFilter


class GetSeedByIdView(RetrieveAPIView):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
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
