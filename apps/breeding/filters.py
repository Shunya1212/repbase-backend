from django_filters import filters
from apps.breeding import models


class BreedingPairFilter(filters.FilterSet):
    class Meta:
        model = models.BreedingPair
        fields = ['male', 'female']


class EggBatchFilter(filters.FilterSet):
    class Meta:
        model = models.EggBatch
        fields = ['breeding_pair']