from rest_framework import generics, response, viewsets
from rest_framework.decorators import action
from apps.feeding import filters, models, serializers


class FoodViewSet(viewsets.ModelViewSet):
    queryset = models.Food.objects.actives()
    serializer_class = serializers.FoodSerializer
    filterset_class = filters.FoodFilter