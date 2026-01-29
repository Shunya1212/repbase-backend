from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.animal import views


router = DefaultRouter()
router.register('animal', views.AnimalViewSet, basename='animal')


urlpatterns = [
    path('', include(router.urls)),
]