from rest_framework import serializers
from .models import Community

class CommunitySerializer(serializers.ModelSerializer):
    #user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Community
        fields= ['id', 'user_id', 'created_at', 'title', 'description', 'img', 'like']
