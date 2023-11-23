from django.utils.module_loading import import_string
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.auth_jwt.serializers        import TokenObtainPairSerializer
from accounts import utils
from django.contrib.auth import update_session_auth_hash

class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def get_serializer_class(self) -> Serializer:
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError:
            msg = "Could not import serializer '%s'" % self._serializer_class
            raise ImportError(msg)

    def get_authenticate_header(self, request: Request) -> str:
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )


class TokenObtainPairView(TokenViewBase):

    serializer_class = TokenObtainPairSerializer

    def _action(self, serializer):
        serializer.is_valid(raise_exception=True)
        utils.login_user(self.request, serializer.user)
        if settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self._action(serializer)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


token_obtain_pair = TokenObtainPairView.as_view()