from urllib.parse import urlparse

import rest_framework.generics as drf_generics
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.order.models import Order

from .serializers import OrderCreateSerializer
from .serializers import OrderSerializer


class OrderListView(drf_generics.ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer


class OrderCreateView(drf_generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        origin = request.META.get("HTTP_ORIGIN")
        referer = request.META.get("HTTP_REFERER")
        allowed_hosts = settings.ALLOWED_HOSTS

        def is_valid_host(url):
            if not url:
                return True
            parsed = urlparse(url)
            return parsed.hostname in allowed_hosts

        if settings.VERIFY_ORIGIN_REFERER:
            if not is_valid_host(origin):
                return Response({"detail": "Invalid origin"},
                                status=status.HTTP_403_FORBIDDEN)

        if not is_valid_host(referer):
            return Response({"detail": "Invalid referer"},
                            status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)


class OrderUpsertView(drf_generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
