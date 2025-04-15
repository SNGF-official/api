from rest_framework import generics
from rest_framework.permissions import AllowAny

from sngf_api.plant.models import Plant

from .serializers import PlantDetailSerializer
from .serializers import PlantListSerializer


class SeedShopListView(generics.ListAPIView):
    """
    Vue pour lister uniquement les graines.
    """

    permission_classes = [AllowAny]
    serializer_class = PlantListSerializer

    def get_queryset(self):
        return Plant.objects.filter(category=Plant.CategoryChoices.SEED)


class PlantShopListView(generics.ListAPIView):
    """
    Vue pour lister uniquement les plantes.
    """

    permission_classes = [AllowAny]
    serializer_class = PlantListSerializer

    def get_queryset(self):
        return Plant.objects.filter(category=Plant.CategoryChoices.PLANT)


class AllSpeciesShopListView(generics.ListAPIView):
    """
    Vue pour lister toutes les espèces (graines et plantes).
    """

    serializer_class = PlantListSerializer
    permission_classes = [AllowAny]
    queryset = Plant.objects.all()  # Définissez le queryset ici

    def get_queryset(self):
        queryset = self.queryset  # Utilisez le queryset défini au niveau de la classe
        category = self.request.query_params.get("category", None)
        if category:
            queryset = queryset.filter(category=category)

        name = self.request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        status = self.request.query_params.get("status", None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class PlantRetrieveUpdateDestroyView(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
