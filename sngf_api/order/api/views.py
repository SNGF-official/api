import rest_framework.generics as drf_generics
from rest_framework.permissions import AllowAny

from sngf_api.core import generics
from sngf_api.order.models import Order

from .serializers import OrderCreateSerializer
from .serializers import OrderSerializer


class OrderListView(generics.ListCreateUpdateApiView):
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer


class OrderCreateView(drf_generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]
