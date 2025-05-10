from django.db.models import Q


class FilterQueryMixin:
    """
    Mixin pour appliquer des filtres génériques sur un queryset,
    utilisé par les vues Seed et Plant.
    """

    def filter_queryset_by_params(self, queryset, params, extra_filters=None):
        name = params.get("name")
        keyword = params.get("keyword")
        category = params.get("category")
        min_quantity = params.get("minQuantity")
        max_quantity = params.get("maxQuantity")
        min_price = params.get("minPrice")
        max_price = params.get("maxPrice")
        size = params.get("size")

        if name:
            queryset = queryset.filter(name__iexact=name)
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            )
        if category:
            queryset = queryset.filter(category=category)
        if min_quantity:
            queryset = queryset.filter(quantity__gte=int(min_quantity))
        if max_quantity:
            queryset = queryset.filter(quantity__lte=int(max_quantity))
        if min_price:
            queryset = queryset.filter(price_per_kilo__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price_per_kilo__lte=float(max_price))
        if size:
            queryset = queryset.filter(prices__size=size)

        if extra_filters:
            queryset = queryset.filter(**extra_filters)

        return queryset.distinct()
