import rest_framework.generics as drf_generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.core import generics
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
        allowed = "https://sngf-silo.com"

        if origin and not origin.startswith(allowed):
            return Response({"detail": "Invalid origin"}, status=403)

        if referer and not referer.startswith(allowed):
            return Response({"detail": "Invalid referer"}, status=403)

        return super().create(request, *args, **kwargs)
