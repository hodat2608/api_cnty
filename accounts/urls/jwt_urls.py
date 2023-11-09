from django.urls import re_path
from rest_framework_simplejwt import views
from accounts.auth_jwt.views import TokenObtainPairView

urlpatterns = [
    re_path(r"^jwt/create/?", 
        views.TokenObtainPairView.as_view(), 
            name="jwt-create"),

    re_path(r"^jwt/refresh/?", 
        views.TokenRefreshView.as_view(), 
            name="jwt-refresh"),

    re_path(r"^jwt/verify/?", 
        views.TokenVerifyView.as_view(), 
            name="jwt-verify"),

    re_path(r"^jwt/custom/?", 
        TokenObtainPairView.as_view(), 
            name="jwt-custom"),


]
