from django.urls import path
from . import views


urlpatterns = [
    path('', views.users, name='users'),
    path('account/', views.account, name='account'),
    path('<str:pk>', views.user, name='user'),

    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),

    path('edit-author/<str:pk>', views.authorEdit, name='edit-author'),

    path('create-interest/', views.interestCreate, name='create-interest'),
    path('edit-interest/<str:pk>', views.interestEdit, name='edit-interest'),
    path('delete-interest/<str:pk>', views.interestDelete, name='delete-interest'),

    path('output-messages/', views.outputMessages, name='output'),
    path('input-messages/', views.inputMessages, name='input'),
    path('message/<str:pk>', views.currentMessage, name='message'),
    path('create-message/<str:pk>', views.createMessage, name='create-message'),





]