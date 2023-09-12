from django.urls import path,include
from accounts.views import UserViewSet,SetViews,verify_email_api_view,VerifyViaEmailViews,ChangePasswordView,change_password_api

urlpatterns = [
    path('signup_backup/', UserViewSet.as_view({'post': 'signup_backup'}), name='signup_backup'),
    path('signup/', UserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('auth_token/', SetViews.as_view(), name='auth'),
    path('verify_email_api_view/<str:uidb64>/<str:token>/', verify_email_api_view, name='verify_email_api_view'),
    path('VerifyViaEmailViews/<str:uidb64>/<str:token>/', VerifyViaEmailViews.as_view(), name='VerifyViaEmailViews'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-password-api/', change_password_api, name='change-password-api'),
]

