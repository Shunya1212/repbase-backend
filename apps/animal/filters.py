import django_filters as filters
from django.db.models import TextChoices, Q, Case, When, IntegerField
from apps.animal import models


class AnimalFilter(filters.FilterSet):
    code = filters.CharFilter(lookup_expr='icontains')
    ordering = filters.OrderingFilter(
        fields=(
            ('code', 'code'),
        )
    )

    class Meta:
        model = models.Animal
        fields = ['specie', 'sex', 'origin', 'egg', 'status', 'is_assist_feed_needed']