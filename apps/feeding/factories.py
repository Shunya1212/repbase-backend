import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from apps.feeding import models


class FoodFactory(DjangoModelFactory):
    name = factory.Faker('word')
    type = FuzzyChoice(models.Food.Type.choices)
    unit = FuzzyChoice(models.Food.Unit.choices)

    class Meta:
        model = models.Food