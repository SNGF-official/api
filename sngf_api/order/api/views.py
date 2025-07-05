from urllib.parse import urlparse

from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sngf_api.order.models import Order
from .serializers import OrderCreateSerializer, OrderSerializer



def is_valid_host(url: str | None) -> bool:
    if not url:
        return True
    parsed = urlparse(url)
    hostname = parsed.hostname
    return hostname and any(
        hostname == allowed or hostname.endswith(f".{allowed}")
        for allowed in settings.ALLOWED_HOSTS
    )

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class OrderUpsertView(APIView):
    """
    Idempotent create or update an order via PUT on /orders/
    """
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        origin = request.META.get("HTTP_ORIGIN")
        referer = request.META.get("HTTP_REFERER")

        if settings.VERIFY_ORIGIN_REFERER:
            if not is_valid_host(origin):
                return Response({"detail": "Invalid origin"}, status=status.HTTP_403_FORBIDDEN)
            if not is_valid_host(referer):
                return Response({"detail": "Invalid referer"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        order_id = data.get("id")

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                serializer = OrderCreateSerializer(order, data=data, partial=True)
            except Order.DoesNotExist:
                serializer = OrderCreateSerializer(data=data)
        else:
            serializer = OrderCreateSerializer(data=data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPutByIdView(generics.UpdateAPIView):
    """
    PUT /orders/{id} to update an existing order
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
