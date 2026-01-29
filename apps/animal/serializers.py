from rest_framework import serializers
from apps.animal import models


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = '__all__'