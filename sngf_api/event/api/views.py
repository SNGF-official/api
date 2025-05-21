import rest_framework.generics as drf_spectacular
from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.event.api.serializers import EventSerializer
from sngf_api.event.models import EventModel


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


class GetEventByIdView(drf_spectacular.RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class GetListEventView(drf_spectacular.ListAPIView):
    serializer_class = EventSerializer
    pagination_class = FlatListPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = EventModel.objects.all()

        keyword = self.request.query_params.get("keyword")
        date_str = self.request.query_params.get("date")

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )

        if date_str:
            try:
                date = parse_date(date_str)
                if date:
                    queryset = queryset.filter(date__date=date)
            except (ValueError, TypeError):
                pass

        return queryset
