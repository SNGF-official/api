from django.urls import path

from sngf_api.blog.api.views import BlogListView

urlpatterns = [
    path("blogs/", BlogListView.as_view(), name="blogs"),
]
