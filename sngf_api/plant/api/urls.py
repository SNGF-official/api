from django.urls import path

from .views import GetListPlantView, GetCategoriesView
from .views import GetListSeedView
from .views import GetPlantByIdView
from .views import GetSeedByIdView

urlpatterns = [
    path("plants/", GetListPlantView.as_view(), name="plant-list"),
    path("plants/<uuid:id>/", GetPlantByIdView.as_view(), name="plant-detail"),
    path("seeds/", GetListSeedView.as_view(), name="seed-list"),
    path("seeds/<uuid:id>/", GetSeedByIdView.as_view(), name="seed-detail"),
    path("categories/", GetCategoriesView.as_view(), name="get-categories"),
]
