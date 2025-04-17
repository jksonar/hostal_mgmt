from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('allocate/', views.allocate_room, name='allocate_room'),
    path('request-room/', views.request_room, name='request_room'),
    path('view-requests/', views.view_requests, name='view_requests'),
    path('register/', views.register, name='register'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
]
