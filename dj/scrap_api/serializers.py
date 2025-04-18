
from rest_framework import serializers
from .models import CricketMatch


class CricketMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CricketMatch
        fields = '__all__'
