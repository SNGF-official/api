from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sngf_api.files.models import FileModel

# ruff : noqa: N815


class UploadRawFileSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(
        max_length=250,
        validators=[UniqueValidator(queryset=FileModel.objects.all())],
    )
    type = serializers.CharField(max_length=250)
    file = serializers.ListField(
        child=serializers.IntegerField(),
    )
    createdAt = serializers.DateTimeField(source="created_at", required=False)

    class Meta:
        fields = (
            "id",
            "name",
            "type",
            "createdAt",
            "file",
        )

    def create(self, validated_data):
        return FileModel.objects.create(**validated_data)


class UploadFileSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(
        max_length=250,
        validators=[UniqueValidator(queryset=FileModel.objects.all())],
    )
    type = serializers.CharField(max_length=250)
    createdAt = serializers.DateTimeField(source="created_at", required=False)

    class Meta:
        fields = (
            "id",
            "name",
            "type",
            "createdAt",
            "file",
        )

    def create(self, validated_data):
        return FileModel.objects.create(**validated_data)
