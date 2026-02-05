from django.http import Http404
from rest_framework import generics, viewsets
from apps.animal import models, serializers, filters


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = models.Animal.objects.actives()
    serializer_class = serializers.AnimalSerializer
    filterset_class = filters.AnimalFilter