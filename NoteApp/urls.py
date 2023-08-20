from django.urls import path
from . import views 


urlpatterns = [
    path('', views.getRouter),
    path('All_Note/', views.getNote),
    path('Action/<str:id>/', views.detail_note),
]