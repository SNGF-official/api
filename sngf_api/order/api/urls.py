from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView,
    OrderUpsertView,
    OrderPutByIdView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("<uuid:id>/", OrderDetailView.as_view(), name="order-detail"),
    path("<uuid:id>", OrderPutByIdView.as_view(), name="order-update-id"),
    path("", OrderUpsertView.as_view(), name="order-upsert"),
]
