from rest_framework import serializers
from apps.specie import models


class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specie
        fields = '__all__'


class GrowthStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GrowthState
        fields = '__all__'