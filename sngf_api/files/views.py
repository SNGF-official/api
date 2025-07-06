from typing import TYPE_CHECKING

from django.core.files.base import ContentFile
from django.http.response import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics as drf_generics
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sngf_api.files.filters import FileResourceFilter
from sngf_api.files.models import FileModel
from sngf_api.files.serializers import UploadFileSerializer
from sngf_api.files.serializers import UploadRawFileSerializer

if TYPE_CHECKING:
    from rest_framework.serializers import BaseSerializer


class UploadRawFileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UploadRawFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        _type = validated_data.get("type", None)
        name = validated_data.get("name", None)
        file_to_upload = validated_data.get("file", None)

        file_name_with_extension = f"{name}.{_type}"
        file = ContentFile(bytes(file_to_upload), name=file_name_with_extension)
        saved_file = FileModel(file=file, name=name, type=_type)
        saved_file.save()

        serializer = UploadFileSerializer(saved_file, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadFileView(drf_generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = FileModel.objects.all()
    serializer_class = UploadFileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FileResourceFilter

    def post(self, request, *args, **kwargs):
        file = request.data.get("fileToUpload")
        if not file:
            return Response(
                {"detail": "No file was uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        data["name"] = (
            file.name if not request.data.get("name") else request.data.get("name")
        )

        serializer: BaseSerializer[UploadFileSerializer] = self.get_serializer(
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileUploadDetailsView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = FileModel.objects.all()
    serializer_class = UploadFileSerializer


class FileDownloadDetailsView(RetrieveAPIView):
    queryset = FileModel.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        file: FileModel = self.get_object()
        return FileResponse(file.file.open(), filename=file.name, as_attachment=True)
