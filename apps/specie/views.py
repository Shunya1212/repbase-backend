from django.shortcuts import render
from rest_framework import viewsets
from apps.specie import models, serializers, filters


class GrowthStateViewSet(viewsets.ModelViewSet):
    queryset = models.GrowthState.objects.actives()
    serializer_class = serializers.GrowthStateSerializer
    filterset_class = filters.GrowthStateFilter