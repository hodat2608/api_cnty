from django.urls import path
from accounts.views import UserViewSet,SetViews,verify_email
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'auth_system'
urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'signup'}), name='signup'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('auth_token/', SetViews.as_view(), name='auth'),
    path('verify_email/<str:uidb64>/<str:token>/', UserViewSet.as_view({'get': 'verify_email'}), name='verify_email'),
]

