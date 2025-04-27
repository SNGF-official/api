from django.urls import path

from sngf_api.order.api.views import OrderCreateView
from sngf_api.order.api.views import OrderDeleteView
from sngf_api.order.api.views import OrderDetailView
from sngf_api.order.api.views import OrderListView
from sngf_api.order.api.views import OrderUpdateView

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<uuid:id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<uuid:id>/update/", OrderUpdateView.as_view(), name="order-update"),
    path("orders/<uuid:id>/delete/", OrderDeleteView.as_view(), name="order-delete"),
]
