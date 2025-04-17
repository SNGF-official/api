import rest_framework.generics as drf_spectacular
from django.utils.dateparse import parse_date
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.blog.api.serializers import BlogSerializer
from sngf_api.blog.models import Blog
from sngf_api.core.models import Status


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


class GetListBlogView(drf_spectacular.ListAPIView):
    queryset = Blog.objects.filter(status=Status.STATUS.ACTIVE)
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = FlatListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get("keyword")
        status = self.request.query_params.get("status")
        published_date = self.request.query_params.get("publishedAt")

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if status:
            queryset = queryset.filter(status=status)
        if published_date:
            date = parse_date(published_date)
            if date:
                queryset = queryset.filter(published_at__date=date)

        return (
            queryset.filter(status=Status.STATUS.ACTIVE)
            .distinct()
            .order_by("-published_at")
        )


class GetBlogByIdView(drf_spectacular.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
