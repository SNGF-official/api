from django.urls import path

from sngf_api.files.views import FileDownloadDetailsView
from sngf_api.files.views import FileUploadDetailsView
from sngf_api.files.views import UploadFileView
from sngf_api.files.views import UploadRawFileView

urlpatterns = [
    path("files/", UploadFileView.as_view(), name="files"),
    path("files/<uuid:pk>/", FileUploadDetailsView.as_view(), name="file-details"),
    path(
        "files/<uuid:pk>/download/",
        FileDownloadDetailsView.as_view(),
        name="file-download-details",
    ),
    path("files/raw/", UploadRawFileView.as_view(), name="raw-file"),
]
