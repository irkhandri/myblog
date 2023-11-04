from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blogs.models import Blog, Comment, Tag
from django.contrib.auth.models import User
from users.models import Author


class BlogTest(APITestCase):

    # def test_view_blog(self):

    #     url = reverse('api:list')
    #     response = self.client.get(url, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_create_blog(self):

    #     # self.test_tag = Tag.objects.get(name='testing')
        
    #     test_user1 = User.objects.create_user(
    #         username='test_user1', password='123123'
    #     )
       
    #     author = Author.objects.create(
    #             user = test_user1,
    #             name = "user.first_name",
    #             email = "user.email",
    #             username = test_user1.username
    #         )
    #     data = {"title" : "title", "description" : "des", 
    #             "owner" : 1
    #             }
    #     url = reverse('api:list')
    #     response = self.client.post(url,data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
