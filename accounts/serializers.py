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
from accounts.combat import get_user_email, get_user_email_field_name
from accounts import views
import time,random
User = get_user_model()

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        instance.email_changed = False
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.email_changed = True
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)
    
class UpdateUsernameSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[settings.LOGIN_FIELD] = serializers.CharField(required=False)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_username")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            if settings.SEND_ACTIVATION_EMAIL:
                user.username = validated_data.get("username")  
                user.is_active = False
                user.save(update_fields=["is_active","username"])
        return user

# class UpdateUsernameSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (settings.LOGIN_FIELD,)       
 
#     def save(self, **kwargs):
#         with transaction.atomic():
#             user = self.context["request"].user
#             user.username = self.validated_data.get(settings.LOGIN_FIELD )
#             user.is_active = False
#             user.save(update_fields=["is_active","username"])
#         return user  
        
class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (settings.EMAIL_FIELD,)        
        
    def save(self, **kwargs):
        with transaction.atomic():
            user = self.context["request"].user
            user.email = self.validated_data.get(
                settings.EMAIL_FIELD
            )
            user.is_active = False
            user.save(update_fields=["is_active","email"])
        return user  
        
class UserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            token = Token.objects.get(user=user)
            function_view_instance = views.FunctionView(self)
            encrypted_token = function_view_instance.encrypt_token(self,str(token))
            timestamp = int(time.time())
            pkid = function_view_instance.generate_otp(self,encrypted_token, timestamp)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                index_of_first_digit = next((index for index, char in enumerate(validated_data.get(settings.EMAIL_FIELD)[:-10]) if char.isdigit()), None)
                if index_of_first_digit is not None:
                    user.username = validated_data.get(settings.EMAIL_FIELD)[:-10][:index_of_first_digit] + str(pkid[1:5])
                user.save(update_fields=["is_active","username",])
        return user
    
class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[settings.EMAIL_FIELD] = serializers.CharField(required=False)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS['messages']['CANNOT_CREATE_USER_ERROR'],   
    }
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            # settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        print('maybe: Model =>>',user)
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return attrs
    
class UserCreatePasswordRetypeSerializer(UserCreateSerializer):
    default_error_messages = {
        "password_mismatch": settings.CONSTANTS['messages']['PASSWORD_MISMATCH_ERROR']
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")
    

class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS['messages']['INVALID_CREDENTIALS_ERROR'],
        "inactive_account": settings.CONSTANTS['messages']['INACTIVE_ACCOUNT_ERROR']
    }
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

    default_error_messages = {
        "invalid_token": settings.CONSTANTS['messages']['INVALID_TOKEN_ERROR'],
        "invalid_uid": settings.CONSTANTS['messages']['INVALID_UID_ERROR'],
    }

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
        
class ActivationSerializer(UidAndTokenSerializer):

    default_error_messages = {
        "stale_token": settings.CONSTANTS['messages']['STALE_TOKEN_ERROR'],
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        raise exceptions.PermissionDenied(self.error_messages["stale_token"])

class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})
    
    default_error_messages = {
        "invalid_password": settings.CONSTANTS['messages']['INVALID_PASSWORD_ERROR'],
    }

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")
        

class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    def validate(self, attrs):
        user = getattr(self, "user", None) or self.context["request"].user
        assert user is not None

        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField(style={"input_type": "password"})
    def validate(self, attrs):

        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            raise serializers.ValidationError({"message": 'password_mismatch'})
    
class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = settings.LOGIN_FIELD
        self._default_username_field = User.USERNAME_FIELD
        self.fields[f"new_{self.username_field}"] = self.fields.pop(self.username_field)

    def save(self, **kwargs):
        if self.username_field != self._default_username_field:
            kwargs[User.USERNAME_FIELD] = self.validated_data.get(
                f"new_{self.username_field}"
            )
        return super().save(**kwargs)


class UsernameRetypeSerializer(UsernameSerializer):
   
    default_error_messages = {
        "username_mismatch": settings.CONSTANTS['messages']['USERNAME_MISMATCH_ERROR'].format(
            settings.LOGIN_FIELD),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_new_" + settings.LOGIN_FIELD] = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        new_username = attrs[settings.LOGIN_FIELD]
        if new_username != attrs[f"re_new_{settings.LOGIN_FIELD}"]:
            self.fail("username_mismatch")
        else:
            return attrs


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        # model = settings.TOKEN_MODEL
        model = Token
        fields = ("auth_token",)


class UserFunctionsMixin:
    def get_user(self, is_active=True):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        if (
            settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
            or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            self.fail("email_not_found")
    
    
class SendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):

    default_error_messages = {
        "email_not_found": settings.CONSTANTS['messages']['EMAIL_NOT_FOUND'],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()


class ChangePasswordSerializer(CurrentPasswordSerializer,PasswordSerializer):
    pass

class ChangePasswordRetypeSerializer(CurrentPasswordSerializer,PasswordRetypeSerializer,):
    pass

class ResetPasswordConfirmSerializer(UidAndTokenSerializer,PasswordSerializer):
    pass

class ResetPasswordConfirmRetypeSerializer(UidAndTokenSerializer, PasswordRetypeSerializer):
    pass

class DeleteUserSerializer(CurrentPasswordSerializer):
    pass

class SetUsernameSerializer( CurrentPasswordSerializer,UsernameSerializer,):
    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD, "current_password")


class SetUsernameRetypeSerializer(SetUsernameSerializer, UsernameRetypeSerializer):
    pass


class UsernameResetConfirmSerializer(UidAndTokenSerializer, UsernameSerializer):
    class Meta:
        model = User
        fields = (settings.LOGIN_FIELD, "uid", "token")
 
class UsernameResetConfirmRetypeSerializer(
    UsernameResetConfirmSerializer, UsernameRetypeSerializer
):
    pass