from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from sngf_api.core.pagination import ResultsPageNumberPagination
from sngf_api.event.api.serializers import EventSerializer
from sngf_api.event.models import EventModel


class EventListViews(ListAPIView):
    serializer_class = EventSerializer
    pagination_class = ResultsPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = EventModel.objects.all().filter(status="ACTIVE").order_by("-date")

        keyword = self.request.query_params.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)

        return queryset


class EventRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = EventSerializer
    queryset = EventModel.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
