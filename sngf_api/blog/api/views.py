import rest_framework.generics as drf_spectacular
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from sngf_api.blog.api.serializers import BlogSerializer
from sngf_api.blog.models import Blog
from sngf_api.core.models import Status


class BlogPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10


class GetListBlogView(drf_spectacular.ListAPIView):
    queryset = Blog.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        from django.utils.dateparse import parse_date

        queryset = super().get_queryset()
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        published_date = self.request.query_params.get("publishedAt")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author=author)

        if published_date:
            date = parse_date(published_date)
            if date:
                queryset = queryset.filter(published_at__date=date)

        return queryset.distinct()


class GetBlogByIdView(drf_spectacular.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
