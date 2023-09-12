from .models import UserAccount
from .serializers import UserSerializer
from rest_framework import viewsets, status
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
from .serializers import UserSerializer
from .tokens import account_activation_token 
from django.utils.encoding import force_str
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer,ResetPasswordEmailSerializer,ResetPasswordEmailConfirmOTPSerializer
from Crypto.Cipher import AES
import base64
import hashlib
import time,random
import os
from django.contrib.sessions.models import Session
import uuid


class FunctionView:

    def __init__(self):
        self.secret_key = os.urandom(32)

    def Activate_via_Email(self,request,user,to_email):
        subject = "Verification Account"
        message = message = render_to_string("static/verify_email.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        from_email = settings.EMAIL_HOST
        send_mail(subject,message,from_email,[to_email])

    def Activate_Email(self,request,user,to_email):
        mail_subject = "Activate your user account."
        message = render_to_string("static/verify_email.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                    received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

    def encrypt_token(self, token):
        block_size = AES.block_size
        cipher = AES.new(self.secret_key, AES.MODE_CBC, os.urandom(16))
        token = token + ' ' * (block_size - len(token) % block_size)
        encrypted_token = cipher.encrypt(token.encode('utf-8'))
        return base64.b32encode(encrypted_token).decode('utf-8')

    def generate_otp(self, encrypted_token, timestamp):
        random_number = random.randint(100000, 999999)
        data_to_hash = f'{encrypted_token}{timestamp}{random_number}'.encode('utf-8')
        sha1_hash = hashlib.sha1(data_to_hash).hexdigest()
        offset = int(sha1_hash[-1], 16)
        truncated_hash = sha1_hash[offset * 2 : offset * 2 + 8]
        otp = int(truncated_hash, 16) % 10**6
        return f'{otp:06}'

    def Activate_Email_by_OTP(self,request,to_email):
        mail_subject = "Verify your account."
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

class VerifyViaEmailViews(viewsets.ViewSet):

    @action(detail=False, methods=['get'])  
    def verify_email(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.activate_account()
            return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email verification link.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post']) 
    def OTP_confirm(request):
        serializer = ResetPasswordEmailConfirmOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = UserAccount.objects.get()
            
     
@api_view(['GET'])
def verify_email_api_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserAccount.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.activate_account()
        return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid email verification link.'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()  
            to_email = user.email
            try:
                FunctionView.Activate_Email(request, user, to_email)
                data['response'] = 'User registered successfully. Please check your email for verification.'
                data['email'] = to_email
                data['username'] = user.username
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                else:
                    token = Token.objects.create(user=user)
                data['token'] = token.key
                data['send_email'] = True 
            except Exception as e:
                data['response_error'] = f'Error sending email: {str(e)}' 
                data['send_email'] = False 
        else:
            data = serializer.errors
            data['email_sent'] = False 
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def signup_backup(self, request):
        serializer = UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user = serializer.save()
            data['response']='User registered successfully'
            data['email'] = user.email
            data['username']= user.username
            token,_ = Token.objects.get_or_create(user=user)
            data['token'] = token.key
        else:
            data=serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request,user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message':'login success' ,'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logout successful'})
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class SetViews(APIView):
    authentication_classes = [BasicAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes =[IsAuthenticated]
    def test_token_api(self, request):
        user = request.user
        return Response({'message': f'{user.username} is allowed to do this work with {user.email}'})
    def get(self, request):
        return self.test_token_api(request)
    def post(self, request):
        return self.test_token_api(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_api(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'message': 'Mật khẩu cũ không chính xác'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get('new_password') != serializer.data.get('re_new_password'):
                return Response({'message': 'Mật khẩu xác nhận không khớp'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user) 
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            re_new_password = serializer.validated_data.get('re_new_password')
            if not old_password or not new_password or not re_new_password:
                return Response({'message': 'Vui lòng điền đầy đủ thông tin'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(old_password):
                return Response({'message': 'Mật khẩu cũ không chính xác'}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != re_new_password:
                return Response({'message': 'Mật khẩu xác nhận không khớp'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': 'Thay đổi mật khẩu thành công'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'])   
    def reset_password(self,request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            email =  serializer.validated_data.get('email')
            if not email:
                data['Response'] = 'You need Email to Reset password'
            try:
                FunctionView.Activate_Email_by_OTP(request,email)
                data['Response'] = "Succsesfully send otp to your email"
                data['send_email'] = True
            except Exception as e:
                data['response_error'] = f'Error sending email: {str(e)}' 
                data['send_email'] = False 
        else:
            data = serializer.errors
            data['email_sent'] = False 
        return Response(data, status=status.HTTP_400_BAD_REQUEST)




            
            
            



