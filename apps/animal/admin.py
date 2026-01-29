from django.contrib import admin
from apps.animal import models


@admin.register(models.Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['code']
    search_fields = ['code']