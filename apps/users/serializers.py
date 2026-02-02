from django.contrib import auth
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import HybridImageField
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from apps.users import models


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    profile_image = HybridImageField(required=False, allow_null=True)
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(), slug_field='name', 
        many=True, allow_empty=True, required=False
    )

    def validate_username(self, value):
        return value.lower()

    def validate_email(self, value):
        UserModel = auth.get_user_model()
        if not self.instance:
            if UserModel.objects.filter(email=value).exists():
                raise serializers.ValidationError("There is already a user with this email.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # ignore password on update
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

    class Meta:
        model = auth.get_user_model()
        depth = 1
        exclude = ['created_by', 'updated_by', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserReadSerializer(serializers.ModelSerializer):
    profile_image = HybridImageField(required=False, allow_null=True)

    class Meta:
        model = auth.get_user_model()
        fields = '__all__'
        read_only_fields = [
            'id', 'created', 'created_by', 'date_joined', 'groups', 'is_active', 'is_staff',
            'is_superuser', 'last_login', 'password', 'user_permissions', 'updated', 'updated_by'
        ]

class CustomAuthTokenSerializer(AuthTokenSerializer):
    user = UserSerializer(read_only=True)

    def validate_username(self, username):
        return username.lower()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            request = self.context.get('request')
            user = auth.authenticate(request=request, username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            auth.login(request, user)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(label='New Password')

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    class Meta:
        model = auth.get_user_model()
        fields = ['new_password']
