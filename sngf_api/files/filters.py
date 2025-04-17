from django_filters import rest_framework as filters

from sngf_api.files.models import FileModel


class FileResourceFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    type = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FileModel
        fields = ["name", "type"]
