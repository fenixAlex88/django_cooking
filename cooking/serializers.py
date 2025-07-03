from rest_framework import serializers

from .models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    """Поля которые будут отображаться в API"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'created_at', 'updated_at', 'content', 'author')

class CategorySerializer(serializers.ModelSerializer):
    """Поля которые будут отображаться в API"""
    class Meta:
        model = Category
        fields = ('id','title', 'posts')