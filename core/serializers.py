from rest_framework import serializers

from .models import Blog, Project, Skill


class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "name", "category_name", "proficiency", "icon", "description"]


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    technologies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail",
            "category_name",
            "technologies",
            "status",
            "github_url",
            "live_url",
        ]


class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "author_name",
            "category_name",
            "featured_image",
            "published_at",
            "views",
        ]

