from rest_framework import status, views, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from django.contrib.auth import logout, get_user_model
from django.http import HttpResponse
from apps.users.serializers import CustomAuthTokenSerializer, UserSerializer, ChangePasswordSerializer


User = get_user_model()


class CustomObtainJSONWebToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={ "request": request }).data
        })


class SignOut(views.APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(status=200)

class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated
        return user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Password reset successfully'})