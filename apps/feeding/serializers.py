from rest_framework import serializers
from apps.feeding import models


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = '__all__'


class FeedingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedingPlan
        fields = '__all__'


class FeedingPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedingPlanItem
        fields = '__all__'