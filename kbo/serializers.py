from rest_framework import serializers
from .models import Hitter, Pitcher, Team

class HitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hitter
        fields = '__all__'

class PitcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitcher
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'