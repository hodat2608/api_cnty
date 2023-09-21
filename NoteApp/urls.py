from django.urls import path,include
from . import views 
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'ownnoteuser', views.ownnoteuser, basename='ownnoteuser')
urlpatterns = [
    path('', views.getRouter),
    path('All_Note/', views.Note_List.as_view()),
    path('Action/<str:pk>/', views.Action.as_view()),

    path('add_note/', views.ownnoteuser.as_view({'post': 'add_note'})),
    path('modify_note/<str:pk>/', views.ownnoteuser.as_view({'put': 'modify_note'})),
    path('delete_note/<str:pk>/', views.ownnoteuser.as_view({'delete': 'delete_note'})),
    path('get_all_note/', views.ownnoteuser.as_view({'get': 'get_all_note'})),
    path('detail_note/<str:pk>/', views.ownnoteuser.as_view({'get': 'detail_note'})),
    path('', include(router.urls)),
]
