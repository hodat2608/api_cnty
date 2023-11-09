# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from django.utils.translation import gettext as _

# from typing import Any, Dict, Optional, Type, TypeVar

# from django.conf import settings
# from django.contrib.auth import authenticate, get_user_model
# from django.contrib.auth.models import AbstractBaseUser, update_last_login
# from django.utils.translation import gettext_lazy as _
# from rest_framework import exceptions, serializers
# from rest_framework.exceptions import ValidationError


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         authenticate_kwargs = {
#             get_user_model().USERNAME_FIELD: attrs.get('username') or attrs.get('email'),
#             'password': attrs.get('password')
#         }
#         try:
#             authenticate_kwargs['request'] = self.context['request']
#         except KeyError:
#             pass

#         self.user = authenticate(**authenticate_kwargs)

#         if not self.user.is_active:
#             raise serializers.ValidationError(_("No active account found with the given credentials"))

#         data = {}

#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         return data
