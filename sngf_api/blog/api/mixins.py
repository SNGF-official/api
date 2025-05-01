from django.db.models import Q
from django.utils.dateparse import parse_date


class BlogFilterMixin:
    """
    Mixin pour appliquer les filtres de recherche sur les blogs :
    - keyword
    - status
    - publishedAt
    """

    def filter_queryset_by_params(self, queryset, params, extra_filters=None):
        keyword = params.get("keyword")
        published_at = params.get("publishedAt")

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )

        if published_at:
            date = parse_date(published_at)
            if date:
                queryset = queryset.filter(published_at__date=date)
        if extra_filters:
            queryset = queryset.filter(**extra_filters)

        return queryset.distinct().order_by("-published_at")
