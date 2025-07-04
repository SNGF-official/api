from django.urls import path

from sngf_api.order.api.views import OrderCreateView, OrderUpsertView
from sngf_api.order.api.views import OrderListView

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<uuid:id>/", OrderUpsertView.as_view(), name="order-upsert"),
]
