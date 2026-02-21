from rest_framework import serializers
from apps.breeding import models


class BreedingPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BreedingPair
        fields = '__all__'


class EggBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EggBatch
        fields = '__all__'