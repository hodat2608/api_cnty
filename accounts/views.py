from .models import UserAccount
from rest_framework import viewsets, status, generics,views
from django.contrib.auth import authenticate,logout,login
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserAccount
from .tokens import account_activation_token 
from django.utils.encoding import force_str
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from Crypto.Cipher import AES
from .serializers import TokenCreateSerializer
import base64
import hashlib
import time,random
from django.utils.timezone import now
import os
from django.contrib.sessions.models import Session
from NoteApp.serializers import NoteSerializer
from NoteApp.models import Note
from accounts import signals, utils
from django.contrib.auth import login, logout
from accounts.combat import get_user_email,get_user_email_field_name
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from accounts.serializers import DeleteUserSerializer
from accounts.serializers import UpdateUsernameSerializer
User = get_user_model()

class FunctionView():
    @staticmethod
    def __init__(self):
        self.secret_key = os.urandom(32)
    @staticmethod
    def encode_email(self,email):
        hex_email = ""
        for char in email:
            hex_char = hex(ord(char))[2:]
            hex_email += hex_char
        return hex_email
    @staticmethod
    def decode_email(self,hex_email):
        email = ""
        hex_pairs = [hex_email[i:i+2] for i in range(0, len(hex_email), 2)]
        for hex_pair in hex_pairs:
            char = chr(int(hex_pair, 16))
            email += char
        return email
    @staticmethod
    def resetpassword_via_Email(self,request,to_email):
        subject = "Reset Password"
        try:
            message = message = render_to_string("static/password_reset_email.html", {
                'domain': get_current_site(request).domain,
                'encrypt_email': self.encode_email(to_email),
                'protocol': 'https' if request.is_secure() else 'http'
            })
        except:
            pass
        encrypt_email = self.encode_email(to_email)
        print(encrypt_email)
        from_email = settings.EMAIL_HOST
        send_mail(subject,message,from_email,[to_email])
    @staticmethod
    def Activate_Email(self,request,user,to_email):
        mail_subject = "Activate your user account."
        message = render_to_string("static/verify_email.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        print(f'http://{get_current_site(request).domain}/VerifyViaEmailViews/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}')
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
        return Response({'message':'Successfully register user account.'})
    @staticmethod
    def encrypt_token(self, token):
        block_size = AES.block_size
        cipher = AES.new(self.secret_key, AES.MODE_CBC, os.urandom(16))
        token = token + ' ' * (block_size - len(token) % block_size)
        encrypted_token = cipher.encrypt(token.encode('utf-8'))
        return base64.b32encode(encrypted_token).decode('utf-8')
    @staticmethod
    def generate_otp(self, encrypted_token, timestamp):
        random_number = random.randint(100000, 999999)
        data_to_hash = f'{encrypted_token}{timestamp}{random_number}'.encode('utf-8')
        sha1_hash = hashlib.sha1(data_to_hash).hexdigest()
        offset = int(sha1_hash[-1], 16)
        truncated_hash = sha1_hash[offset * 2 : offset * 2 + 8]
        otp = int(truncated_hash, 16) % 10**6
        return f'{otp:06}'
    @staticmethod
    def Activate_Email_by_OTP(self,request,to_email):
        mail_subject = "Verify your account with OTP."
        timestamp = int(time.time())
        try:
            user = UserAccount.objects.get(email=to_email)
            token = Token.objects.get(user=user)
            user_token = str(token)
        except UserAccount.DoesNotExist:
            return Response({'message':'Account do not exist'})
        except Token.DoesNotExist:
            return Response({'message':'Token do not exist'})
        encrypted_token = self.encrypt_token(user_token)
        otp = self.generate_otp(encrypted_token, timestamp)
        message = f'Your otp is :{otp}, now you can get otp to reset password'
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            user.is_otp = otp
            user.save()
            messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
   
    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        serializer.is_valid(raise_exception=True)
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        if settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_200_OK
        )
    
    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)

class TokenDestroyView(views.APIView):

    permission_classes = settings.PERMISSIONS.token_destroy

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects.all()
    permission_classes = settings.PERMISSIONS.user
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD
    
    def permission_denied(self, request, **kwargs):
        if (
            settings.HIDE_USERS
            and request.user.is_authenticated
            and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            from rest_framework.exceptions import NotFound
            raise NotFound()
        super().permission_denied(request, **kwargs)


    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset
    
    def get_permissions(self):
        if self.action == "perform_create":
            self.permission_classes = settings.PERMISSIONS.user_create
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "activation":
            self.permission_classes = settings.PERMISSIONS.activation
        elif self.action == "resend_activation":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "reset_password":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "reset_password_confirm":
            self.permission_classes = settings.PERMISSIONS.password_reset_confirm
        elif self.action == "change_password":
            self.permission_classes = settings.PERMISSIONS.change_password
        elif self.action == "set_username":
            self.permission_classes = settings.PERMISSIONS.set_username
        elif self.action == "reset_username":
            self.permission_classes = settings.PERMISSIONS.username_reset
        elif self.action == "reset_username_confirm":
            self.permission_classes = settings.PERMISSIONS.username_reset_confirm
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "perform_create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
            self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.resend_activation
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "change_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.change_password_retype
            return settings.SERIALIZERS.change_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user
        elif self.action == "update_username":
            return settings.SERIALIZERS.update_username
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
       
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])  
    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer, *args, **kwargs):
        super().perform_update(serializer, *args, **kwargs)
        user = serializer.instance
        signals.user_updated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.activation(self.request, context).send(to)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)


    @action(detail=False, methods=['post'])  
    def delete_user(self, request, *args, **kwargs):
        serializer = DeleteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user:
            utils.logout_user(self.request)
        self.perform_destroy(self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])  
    def update_username(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])  
    def activation(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.activate_account()
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not settings.SEND_ACTIVATION_EMAIL or not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {"user": user}
        to = [get_user_email(user)]
        settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)
        
    @action(detail=False, methods=['post'])   
    def reset_password(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post']) 
    def reset_password_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.user.set_password(serializer.validated_data["new_password"])
        serializer.user.save()

        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)

        return Response({'message': 'Thay đổi mật khẩu thành công'}, status=status.HTTP_200_OK)   

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.validated_data['new_password'])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
        
        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        user.save()
        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.username_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SetViews(APIView):
    authentication_classes = [BasicAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes =[IsAuthenticated]
    def test_token_api(self, request):
        user = request.user
        return Response({'message': f'{user.username} is authenticated and be allowed and to work with {user.email}'},status=status.HTTP_200_OK)
    def get(self, request):
        return self.test_token_api(request)
    


