from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sngf_api.order.models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


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
