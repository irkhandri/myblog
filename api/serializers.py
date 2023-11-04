from rest_framework import serializers
from blogs.models import Blog, Tag, Comment
from users.models import Author, Interest, Message
from django.contrib.auth.models import User



class InterstSerializer(serializers.ModelSerializer):
    class Meta :
        model = Interest
        # fields = ["name", "description"]
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CreateUserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create (self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        author = Author.objects.create(
                user = instance,
                name = instance.first_name,
                email = instance.email,
                username = instance.username
            )
        return author



class AuthorSerializer(serializers.ModelSerializer):
    # blogs = BlogSerializer(many=True)
    blogs = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = '__all__'
    
    def get_blogs (self, obj):
        blogs = obj.blog_set.all()
        blogs_ids = [blog.id for blog in blogs]
        #serializer = "BlogSerializer(blogs, many = True).data"
        return blogs_ids

    def get_interests (self, obj):
        interests = obj.interest_set.all()
        serializer = InterstSerializer(interests, many=True).data
        return serializer

class CommentSerializer(serializers.ModelSerializer):
    owner = AuthorSerializer (many=False)

    class Meta:
        model = Comment
        fields = '__all__'



class BlogCreateSerializer (serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'

    def create (self, validated_data):
        tags_data = validated_data.pop('tags')

        blog = Blog.objects.create(**validated_data)

        for tag_data in tags_data:
            tag_name = tag_data.get('name')
            tag, created = Tag.objects.get_or_create(name=tag_name)
            blog.tags.add(tag)

        return blog


class BlogSerializer(serializers.ModelSerializer):
    owner = AuthorSerializer (many=False)
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = '__all__'

    

    def get_comments (self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class MessageSerializer (serializers.ModelSerializer):
    # sender = AuthorSerializer (many=False)

    class Meta:
        model = Message
        fields = '__all__'


