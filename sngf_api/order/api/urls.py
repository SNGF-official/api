from django.urls import path

from .views import (
    OrderDetailView,
    OrderPutByIdView,
    OrderListAndUpsertView, confirm_order,
)

urlpatterns = [
    path("orders/", OrderListAndUpsertView.as_view(), name="order-get-put"),
    path("orders/<uuid:id>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<uuid:id>", OrderPutByIdView.as_view(), name="order-update-id"),
    path("orders/<uuid:id>/confirm/", confirm_order, name="order-confirm"),
]
