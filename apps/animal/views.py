from django.http import Http404
from rest_framework import generics, viewsets
from apps.animal import models, serializers


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer