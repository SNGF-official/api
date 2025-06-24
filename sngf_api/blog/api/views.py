from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sngf_api.blog.api.mixins import BlogFilterMixin
from sngf_api.blog.api.serializers import BlogSerializer
from sngf_api.blog.models import Blog


class FlatListPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"
    max_page_size = 100
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)


class GetListBlogView(BlogFilterMixin, generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = FlatListPagination

    def get_queryset(self):
        queryset = Blog.objects.all()
        return self.filter_queryset_by_params(queryset, self.request.query_params)


class GetBlogByIdView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class CreateBlogView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]


class UpdateBlogView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


class DeleteBlogView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
