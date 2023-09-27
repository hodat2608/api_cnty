from django.urls import path,include
from accounts.views import UserViewSet,SetViews,verify_email_api_view,VerifyViaEmailViews,ChangePasswordView,change_password_api,link_resetpassword_email_api
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'UserViewSet', UserViewSet, basename='UserViewSet')
router.register(r'VerifyViaEmailViews', VerifyViaEmailViews, basename='VerifyViaEmailViews')
router.register(r'ChangePasswordView', ChangePasswordView, basename='ChangePasswordView')
urlpatterns = [
    path('signup_backup/', UserViewSet.as_view({'post': 'signup_backup'}), name='signup_backup'),
    path('signup/', UserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('auth_token/', SetViews.as_view(), name='auth'),
    path('VerifyViaEmailViews/<str:uidb64>/<str:token>/', VerifyViaEmailViews.as_view({'get': 'verify_email'}), name='VerifyViaEmailViews'),
    path('change_password/', ChangePasswordView.as_view({'post': 'change_password'}), name='change_password'),
    path('reset_password/', ChangePasswordView.as_view({'post': 'reset_password'}), name='reset_password'),
    path('reset_password_confirm/<str:encryptemail>/', VerifyViaEmailViews.as_view({'post': 'reset_password_confirm'}), name='reset_password_confirm'),
    path('link_resetpassword_email_api/<str:encryptemail>/', link_resetpassword_email_api, name='link_resetpassword_email_api'),
    path('', include(router.urls)),
]

