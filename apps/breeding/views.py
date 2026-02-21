from rest_framework import viewsets
from apps.breeding import models, serializers, filters


class BreedingPairViewSet(viewsets.ModelViewSet):
    queryset = models.BreedingPair.objects.actives().select_related('male', 'female')
    serializer_class = serializers.BreedingPairSerializer
    filterset_class = filters.BreedingPairFilter


class EggBatchViewSet(viewsets.ModelViewSet):
    queryset = models.EggBatch.objects.actives().select_related('breeding_pair')
    serializer_class = serializers.EggBatchSerializer
    filterset_class = filters.EggBatchFilter