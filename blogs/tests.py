from django.test import TestCase
from blogs.models import Blog, Comment, Tag
from django.contrib.auth.models import User
from users.models import Author



class Test_Create_Blog(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_tag = Tag.objects.create(name='testing')
        test_user1 = User.objects.create_user(
            username='test_user1', password='123123'
        )
       

        author = Author.objects.create(
                user = test_user1,
                name = "user.first_name",
                email = "user.email",
                username = test_user1.username
            )

        test_blog = Blog.objects.create(
            title="Test", description="description", owner_id = 1 
        )

        test_blog.tags.add(test_tag)
        # test_blog.owner = author



        # return super().setUpTestData()
    
    def test_blog (self):
        blog = Blog.objects.get(id=1)
        tag = Tag.objects.get(id=1)
        # print ("!!!!!!!!!!!!!!!!", blog.owner)
        # tag = f'{tag.name}'
        author = f'{blog.owner}'
        title = f'{blog.title}'
        description = f'{blog.description}'
        self.assertEqual(author, 'test_user1')
        self.assertEqual(title, 'Test')
        self.assertEqual(description, 'description')
        self.assertEqual(str(blog), 'Test')
        self.assertEqual(str(author), 'test_user1')
        self.assertEqual(str(tag), 'testing')
