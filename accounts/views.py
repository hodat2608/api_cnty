from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount
from .serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,logout,login
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from allauth.account.utils import send_email_confirmation,setup_user_email
from allauth.account.models import EmailAddress
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,logout,login
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.decorators import action
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from allauth.account.forms import SignupForm
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

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        email = EmailAddress.objects.get(user=user)
        send_email_confirmation(request, email)
        return user

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            email_address = EmailAddress.objects.create(user=user, email=user.email, verified=False, primary=True)
            # setup_user_email(request, user, email_address)
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Activate your account'
            message = render_to_string(
                'static/verify_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user), 
                },
            )
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            send_email_confirmation(request, email_address)
            data['response'] = 'User registered successfully. Please check your email for verification.'
            data['email'] = user.email
            data['username'] = user.username
            if Token.objects.filter(user=user).exists():
                token = Token.objects.get(user=user)
            else:
                token = Token.objects.create(user=user)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def verify_email(self, request, uidb64, token):
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
 
    def signup(self, request):
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
    authentication_classes = [BasicAuthentication,SessionAuthentication]
    permission_classes =[IsAuthenticated]
    def test_token_api(self, request):
        user = request.user
        return Response({'message': f'{user.username} is allowed to do this work with {user.email}'})
    def get(self, request):
        return self.test_token_api(request)
    def post(self, request):
        return self.test_token_api(request)


# @action(detail=False, methods=['get'])
def verify_email(self, request, uidb64, token):
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