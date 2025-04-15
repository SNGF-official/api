from rest_framework import serializers

from sngf_api.blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ["id"]


class BlogListSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, source="miniature")

    class Meta:
        model = Blog
        fields = ["id", "title", "description", "image_url", "published_at", "status"]


class BlogDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ["id"]

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.file.url
        return None
