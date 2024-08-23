from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    community_id = serializers.IntegerField(source='community.id', read_only=True)
    class Meta:
        model = Comment
        fields= ['user_id', 'community_id', 'description', 'like']
