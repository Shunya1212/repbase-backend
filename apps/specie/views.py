from django.shortcuts import render
from rest_framework import viewsets
from apps.specie import models, serializers, filters


class SpecieViewSet(viewsets.ModelViewSet):
    queryset = models.Specie.objects.actives()
    serializer_class = serializers.SpecieSerializer
    filterset_class = filters.SpecieFilter


class GrowthStateViewSet(viewsets.ModelViewSet):
    queryset = models.GrowthState.objects.actives()
    serializer_class = serializers.GrowthStateSerializer
    filterset_class = filters.GrowthStateFilter