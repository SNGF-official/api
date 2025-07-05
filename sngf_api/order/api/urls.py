from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView,
    OrderUpsertView,
    OrderPutByIdView,
)

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<uuid:id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<uuid:id>", OrderPutByIdView.as_view(), name="order-update-id"),
    path("orders/", OrderUpsertView.as_view(), name="order-upsert"),
]
