from django.urls import path
from . import views

urlpatterns = [
     path('lobby/', views.lobby),
     path('room/', views.room),
     path('get_token/', views.getToken),
     path('create_member/', views.createMember),
     path('get_member/', views.getMember),
     path('delete_member/', views.deleteMember),
     path('', views.home),
     path('about/', views.about, name="about"),
     path('contact/', views.contact),
     path('error/', views.error),
     path('login/', views.login),
     path('register/', views.register),
     path('logout/', views.logout),
]
