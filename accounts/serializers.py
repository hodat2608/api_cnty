from rest_framework import serializers
from .models import UserAccount
from rest_framework.authtoken.models import Token
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from django.conf import settings
from accounts import utils
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):

        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs
    
    def create(self, validated_data):
        user = UserAccount(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    # default_error_messages = {
    #     "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
    #     "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[settings.LOGIN_FIELD] = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")

class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    # default_error_messages = {
    #     "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
    #     "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
    # }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )

class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            raise serializers.ValidationError({"message": 'invalid_password'})
        
class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    def validate(self, attrs):
        user = getattr(self, "user", None) or self.context["request"].user
        assert user is not None

        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"message": 'invalid_form_password'})
        return super().validate(attrs)

class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField(style={"input_type": "password"})
    def validate(self, attrs):

        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            raise serializers.ValidationError({"message": 'password_mismatch'})
    

class ResetPasswordEmailSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    re_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        re_new_password = attrs.get('re_new_password')
        if not new_password or not re_new_password :
            raise serializers.ValidationError({'message': 'Vui lòng điền đầy đủ thông tin'})
        if new_password != re_new_password:
            raise serializers.ValidationError({'message': 'Password and password confirmation do not match'})
        return super().validate(attrs)
    
class Email_password(serializers.Serializer):
    email = serializers.EmailField(required=True) 

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({'message': 'We need email???'})
        if not UserAccount.objects.filter(email=email).exists:
            raise serializers.ValidationError({'message': 'Email do not exists'})
        return super().validate(attrs)
    
class ChangePasswordSerializer(PasswordRetypeSerializer,CurrentPasswordSerializer):
    pass