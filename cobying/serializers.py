from rest_framework import serializers
from .models import Cobying

class CobyingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cobying
        fields = "__all__"