from django.urls import path

from .views import AllSpeciesShopListView
from .views import PlantRetrieveUpdateDestroyView
from .views import PlantShopListView
from .views import SeedShopListView

urlpatterns = [
    path("shop/seeds/", SeedShopListView.as_view(), name="seed-shop"),
    path("shop/plants/", PlantShopListView.as_view(), name="plant-shop"),
    path("plants/", AllSpeciesShopListView.as_view(), name="all-species-shop"),
    path(
        "plants/<uuid:id>/",
        PlantRetrieveUpdateDestroyView.as_view(),
        name="plant-detail",
    ),
]
