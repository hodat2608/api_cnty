from django.urls import path
from . import views 
from rest_framework.urlpatterns import format_suffix_patterns


# urlpatterns = [
#     path('', views.getRouter),
#     path('All_Note/', views.getNote),
#     path('Action/<str:id>/', views.detail_note),
# ]

urlpatterns = [
    path('', views.getRouter),
    path('All_Note/', views.Note_List.as_view()),
    path('Action/<str:pk>/', views.Action.as_view()),
]
