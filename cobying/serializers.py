from rest_framework import serializers
from .models import Cobying, HashTag

class CobyingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobying
        fields = "__all__"

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['id', 'hashtag']