from django.urls import path,include
from accounts.views import UserViewSet,SetViews,verify_email_api_view,VerifyViaEmailViews,ChangePasswordView,change_password_api,link_resetpassword_email_api

urlpatterns = [
    path('signup_backup/', UserViewSet.as_view({'post': 'signup_backup'}), name='signup_backup'),
    path('signup/', UserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('auth_token/', SetViews.as_view(), name='auth'),
    path('VerifyViaEmailViews/<str:uidb64>/<str:token>/', VerifyViaEmailViews.as_view({'get': 'verify_email'}), name='VerifyViaEmailViews'),
    path('change_password/', ChangePasswordView.as_view({'post': 'change_password'}), name='change_password'),
    path('reset_password/', ChangePasswordView.as_view({'post': 'reset_password'}), name='reset_password'),
    path('link_resetpassword_email/<str:encrypt_email>/', VerifyViaEmailViews.as_view({'post': 'link_resetpassword_email'}), name='link_resetpassword_email'),
    path('link_resetpassword_email_api/<str:encryptemail>/', link_resetpassword_email_api, name='link_resetpassword_email_api'),
]

