from rest_framework import serializers
from apps.feeding import models


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = '__all__'