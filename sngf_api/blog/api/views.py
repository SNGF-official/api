from rest_framework import generics
from rest_framework.permissions import AllowAny

from sngf_api.blog.models import Blog

from .serializers import BlogListSerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all().filter(status="ACTIVE")
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
