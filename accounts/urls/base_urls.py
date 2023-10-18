from django.urls import path,include
from accounts import views
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
User = get_user_model()
router = DefaultRouter()
router.register("users", views.UserViewSet, basename='users')
urlpatterns = router.urls
