from rest_framework import serializers
from apps.specie import models


class GrowthStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GrowthState
        fields = '__all__'