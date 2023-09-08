from rest_framework import serializers
from .models import UserAccount
from rest_framework.authtoken.models import Token
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ('id', 'email', 'username', 'password','password_confirm')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        user = UserAccount(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Invalid password confirm'})
        user.set_password(password)
        user.save()
        return user


