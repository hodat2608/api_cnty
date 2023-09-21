from rest_framework import serializers
from .models import UserAccount
from rest_framework.authtoken.models import Token
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from django.contrib.auth import update_session_auth_hash

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'username', 'password','password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Password and password confirmation do not match'})
        return data

    def create(self, validated_data):
        user = UserAccount(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    re_new_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        re_new_password = data.get('re_new_password')
        user = self.context.get("user")
        if not old_password or not new_password or not re_new_password:
            raise serializers.ValidationError({'message': 'Vui lòng điền đầy đủ thông tin'})
        if new_password != re_new_password:
            raise serializers.ValidationError({'message': 'Password and password confirmation do not match'})
        if not user.check_password(old_password):
            raise serializers.ValidationError({'message': 'Wrong password'})
        return data

class ResetPasswordEmailSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    re_new_password = serializers.CharField(required=True)

class Email_password(serializers.Serializer):
    email = serializers.EmailField(required=True) 