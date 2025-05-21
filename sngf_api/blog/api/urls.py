from django.urls import path

from sngf_api.blog.api.views import GetBlogByIdView
from sngf_api.blog.api.views import GetListBlogView

urlpatterns = [
    path("blogs/", GetListBlogView.as_view(), name="blog-list"),
    path("blogs/<uuid:id>/", GetBlogByIdView.as_view(), name="blog-detail"),
]
