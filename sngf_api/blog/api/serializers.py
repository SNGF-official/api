from rest_framework import serializers

from sngf_api.blog.models import Blog

# ruff : noqa : N815


class BlogSerializer(serializers.ModelSerializer):
    imageUrl = serializers.ImageField(source="miniature")
    publishedAt = serializers.DateTimeField(source="published_at")
    fileId = serializers.PrimaryKeyRelatedField(source="file", read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "imageUrl", "description", "publishedAt", "fileId"]
        read_only_fields = ["id"]
