from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from social_django.utils import load_backend, load_strategy

from django.conf import settings
# from accounts.auth_social.serializers import ProviderAuthSerializer


class ProviderAuthView(generics.CreateAPIView):
    permission_classes = settings.PERMISSIONS.activation
    serializer_class = settings.SERIALIZERS.o_auth2

    def get(self, request, *args, **kwargs):
        redirect_uri = request.GET.get("redirect_uri")
        if redirect_uri not in settings.SOCIAL_AUTH_ALLOWED_REDIRECT_URIS:
            return Response(
                "redirect_uri must be in SOCIAL_AUTH_ALLOWED_REDIRECT_URIS",
                status=status.HTTP_400_BAD_REQUEST,
            )
        strategy = load_strategy(request)
        strategy.session_set("redirect_uri", redirect_uri)

        backend_name = self.kwargs["provider"]
        backend = load_backend(strategy, backend_name, redirect_uri=redirect_uri)

        authorization_url = backend.auth_url()
        return Response(data={"authorization_url": authorization_url})
