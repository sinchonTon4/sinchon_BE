from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields= ['id', 'user_id', 'community_id', 'description', 'like']
