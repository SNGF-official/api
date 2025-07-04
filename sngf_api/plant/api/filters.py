from django.db.models import Q
from django_filters import rest_framework as filters

from sngf_api.plant.models import Plant, Seed


class PlantFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    keyword = filters.CharFilter(method="filter_by_keyword")
    category = filters.CharFilter(field_name="categories__name", lookup_expr="exact")
    size = filters.CharFilter(field_name="prices__size", lookup_expr="exact")
    minQuantity = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    maxQuantity = filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    minPrice = filters.NumberFilter(field_name="prices__price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="prices__price", lookup_expr="lte")

    class Meta:
        model = Plant
        fields = []

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class SeedFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    keyword = filters.CharFilter(method="filter_by_keyword")
    category = filters.CharFilter(field_name="categories__name", lookup_expr="exact")
    minQuantity = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    maxQuantity = filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    minPrice = filters.NumberFilter(field_name="price_per_kilo", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price_per_kilo", lookup_expr="lte")

    class Meta:
        model = Seed
        fields = []

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
