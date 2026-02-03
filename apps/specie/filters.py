import django_filters as filters
from apps.specie import models


class GrowthStateFilter(filters.FilterSet):
    class Meta:
        model = models.GrowthState
        fields = []