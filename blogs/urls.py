from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('blog/<int:pk>/', views.blog, name='blog'),
    path('create-blog/', views.createBlog, name='create-blog'),
    path('update-blog/<int:pk>/', views.updateBlog, name='update-blog'),
    path('delete-blog/<int:pk>/', views.deleteBlog, name='delete-blog'),
    
]