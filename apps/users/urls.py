from django.urls import path, include
from apps.users import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.CustomObtainJSONWebToken.as_view(), name='api-token-auth'),
    path('sign-out/', views.SignOut.as_view(), name='sign-out'),
    # path('register-notification-token/', views.RegisterNotificationTokenView.as_view(), name='register-notification-token'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
]
