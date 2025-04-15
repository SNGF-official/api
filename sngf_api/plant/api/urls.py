from django.urls import path

from .views import GetListPlantView
from .views import GetPlantByIdView

urlpatterns = [
    path("plants/", GetListPlantView.as_view(), name="plant-list"),
    path("plants/<uuid:id>/", GetPlantByIdView.as_view(), name="plant-detail"),
]
