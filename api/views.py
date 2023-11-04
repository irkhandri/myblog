from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import BlogSerializer, TagSerializer, AuthorSerializer, InterstSerializer, MessageSerializer, BlogCreateSerializer, CreateUserSerializer
from blogs.models import Blog, Tag, Comment
from users.models import Author, Interest, Message

from rest_framework import generics, status, viewsets ,filters
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from django.db.models import Q






@api_view(['GET'])
def getRoutes (request):

    routes = [

        {'GET':'/api/blogs'},
        {'GET':'/api/blogs/id'},
        {"GET" : "/api/users/token/"},
        {'GET' : "/api/users/token/refresh/"},
        {"POST" : "/api/blogs/<pk>/comment/"} ,
        {'GET, PUT, DELETE' : "/api/blogs/<pk>"},
        {"POST" : "/api/blogs/create/"},
        {"GET" : "/api/blogs/search"},
        {'GET, POST' : '/api/tags/'},
        {'POST' : '/api/users/register/' },
        {'GET' : "/api/users/search/"},
        {'GET, POST' : "users/<pk>/interests/"},
        {'GET, POST, DELETE' : "users/<pk>/interests/<interest_id>/"},
        {'GET' : "/api/input-messages/"},
        {'GET' : "/api/output-messages/"},
        {"POST" : "/api/create-message/<pk>"},

        {'GET' : "/api/docs/"},
        {'GET' : "/api/schema/"},
        







        # {'GET':'/api/blogs/tags/'},
        # {'POST':'/api/blogs/tags/create/'},

        # {'POST':'/api/blogs/id/comment'},

        

        # {'POST':'/api/users/token'},
        # {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes)


# _________________________________________________________________________________________________________________
#  PERMISSIONS

class BlogUserWritePermission (BasePermission):
    message = 'Only author can edit blog.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        try :
            author = request.user.author
        except:
            return False
        
        return author== obj.owner
    

class AuthorWritePermission (BasePermission):
    message = 'You can edit only your account'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_authenticated:
            return request.user.author == obj
        return False

class InterestWriterPermission (BasePermission):
    message = "You can edit only yours interests"

    def has_object_permission (self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        try:
            author = request.user.author
        except:
            return False
        
        request.kwargs.get('pk')

        return author.id == request.data.get('pk')



class IsAdminOrReadOnly(BasePermission):
    message = "Only admin can edit/delete Tags"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff 


# _________________________________________________________________________________________________________________
# BLOG/S

class BlogSer(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [BlogUserWritePermission]


    def create(self, request, *args, **kwargs):
        raise PermissionDenied("POST method is not allowed for this resource.")
    


@permission_classes([IsAuthenticated])
class BlogCreate (generics.CreateAPIView):
    serializer_class = BlogCreateSerializer

    def perform_create(self, serializer):
        owner = self.request.user.author
        serializer.save(owner=owner)


#  SEARCHING
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__name', 'owner__name']


# COMMENT

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blogComment (request, pk):

    author = request.user.author
    blog = Blog.objects.get(id=pk)

    data = request.data

    if blog.owner == author:
        return Response(
            {"error": "CANT COMMENT OWN BLOG"},
            status=status.HTTP_400_BAD_REQUEST 
        )
    if author.id in blog.commentators:
        return Response(
            {"error": "CAN COMMENT ONLY ONCE"},
            status=status.HTTP_400_BAD_REQUEST 
        )
    
    for vote in  Comment.vote_set:
        if data["react"]  in vote:
            comment = Comment.objects.create(
                blog = blog,
                owner = author,
                react = data["react"],
                description = data["description"]
            )
            comment.save()

            blog.countReaction
            

            serializer = BlogSerializer(blog, many=False)
            return Response(serializer.data)
    




# _________________________________________________________________________________________________________________
# # TAG

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# _________________________________________________________________________________________________________________
#  AUTHOR / USER


class AuthorList (viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AuthorWritePermission]

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("POST method is not allowed for this resource.")
    



# SEARCHING

#  jenom abych zkusil
@api_view(["GET"])
def AuthorSearching (request):
    some_query = request.query_params.get('search')
        # authors = Author.objects.filter(id=some_query)

    interests = Interest.objects.filter(name__iexact = some_query)

    authors = Author.objects.distinct().filter(
            Q(name__icontains = some_query) |
            Q(email__icontains = some_query) |
            Q(username__icontains = some_query) |
            Q(location__icontains = some_query) |
            Q(intro__icontains = some_query) |
            Q(bio__icontains = some_query) |
            Q(interest__in = interests)
        )

        # print(some_query)
    return Response(AuthorSerializer(authors, many=True).data)
        



class UserCreate (APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# _________________________________________________________________________________________________________________
# INTERESTS


class InterestList(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterstSerializer
    permission_classes = [InterestWriterPermission]

    def list (self, request, pk):
        # owner_id = request.get('pk')
        author = Author.objects.get(id = pk)
        queryset = author.interest_set.all()
        serializer = InterstSerializer(queryset, many=True).data
        return Response(serializer)
    

    def retrieve (self, request, pk=None, interest_id=None):
        queryset = Interest.objects.get(id=interest_id)
        return Response(InterstSerializer(queryset, many=False).data)
        
    def create (self, request, pk=None):
        author = Author.objects.get(id=pk)
        data = {
            "name" : request.data.get('name'),
            "description" : request.data.get('description'),
            "owner" : author.id
        }        
        serializer = InterstSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy (self,request,pk, interest_id):
        author = Author.objects.get(id=pk)
        interest = Interest.objects.get(id=interest_id)
        if interest.owner == author:
            interest.delete()
        else:
            return  Response( status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def update(self, request, pk=None, interest_id=None):
        author = Author.objects.get(id=pk)

        try:
            interest = author.interest_set.get(pk=interest_id)
        except Interest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        serializer = InterstSerializer(instance=interest, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
# _________________________________________________________________________________________________________________
#  MEsSAGES


@permission_classes([IsAuthenticated])
class MessageInputList (generics.ListAPIView):

    serializer_class = MessageSerializer

    def get_queryset(self):
        author = self.request.user.author
        messages = author.messages.all()
        return messages


@permission_classes([IsAuthenticated])
class MessageOutputList (generics.ListAPIView):

    serializer_class = MessageSerializer

    def get_queryset(self):
        author = self.request.user.author
        messages = author.out_messages.all()
        return messages


@permission_classes([IsAuthenticated])
class CreateMessage (generics.CreateAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        sender = None
        recipient = Author.objects.get(id = self.kwargs.get('pk'))

        if self.request.user.is_authenticated:
            sender = self.request.user.author
            serializer.save(sender=sender, recipient=recipient, email=sender.email, name=sender.name)
        else:
            serializer.save(sender=sender, recipient=recipient)




#  ------------------------------------------------------------------------------------------


# class BlogDetail (generics.RetrieveUpdateDestroyAPIView, BlogUserWritePermission):
#     permission_classes = [BlogUserWritePermission]
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer

#     # permission_classes = 


# class BlogList (generics.ListAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer

#     def perform_create(self, serializer):
#         owner = self.request.user.author
#         serializer.save(owner = owner)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def blogComment(request, pk):
#     blog = Blog.objects.get(id=pk)
#     author = request.user.author
#     data = request.data


#     if blog.owner == author:
#         return Response(
#             {"error": "CANT COMMENT OWN BLOG"},
#             status=status.HTTP_400_BAD_REQUEST 
#         )
    
#     if author.id in blog.commentators:
#         return Response(
#             {"error": "CAN COMMENT ONLY ONCE"},
#             status=status.HTTP_400_BAD_REQUEST 
#         )

    
#     for vote in  Comment.vote_set:
#         if data["react"]  in vote:
#             comment = Comment.objects.create(
#                 blog = blog,
#                 owner = author,
#                 react = data["react"],
#                 description = data["description"]
#             )
#             comment.save()

#             blog.countReaction
            

#             serializer = BlogSerializer(blog, many=False)
#             return Response(serializer.data)
    

#     return Response(
#         {"error": "WRONG REACTION"},
#         status=status.HTTP_400_BAD_REQUEST 
#     )
    



# class BlogList(generics.ListAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     authentication_classes = [authentication.TokenAuthentication ]



# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def getBlogs (request):
#     blogs = Blog.objects.all()
#     serializer = BlogSerializer(blogs, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def getBlog (request, pk):
#     blog = Blog.objects.get(id=pk)
#     serializer = BlogSerializer(blog, many=False)
#     return Response(serializer.data)


# @permission_classes([IsAuthenticated])
# class CreateBlog (generics.CreateAPIView):
#     serializer_class = BlogSerializer

#     def perform_create(self, serializer):
#         owner = self.request.user.author
#         serializer.save(owner = owner)

        



# #  AUTHOR / S

# class AuthorsList(generics.ListAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

# class AuthorView(generics.RetrieveAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer


# @permission_classes([IsAuthenticated])
# class UpdateAuthor(generics.UpdateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

#     def perform_update(self, serializer):
#         author = self.request.user.author
#         if author.id != self.kwargs.get('pk'):
#             print("!!!!!!!!!")
#             return Response(
#                     {"errwor": "WRONG ID"},
#                     status=status.HTTP_400_BAD_REQUEST 
#             )        
#         serializer.save()






# @permission_classes([IsAuthenticated])
# class CreateTag(generics.CreateAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer



# # INTEREST
# class InterestList(generics.ListAPIView):
#     # queryset = Interest.objects.all()
#     serializer_class = InterstSerializer

#     def get_queryset(self):
#         author_id = self.kwargs.get('pk')
#         author = get_object_or_404(Author, id = author_id) 
#         interests = Interest.objects.filter(owner = author)
#         return interests


# @permission_classes([IsAuthenticated])
# class CreateInterest (generics.CreateAPIView):
#     serializer_class = InterstSerializer

#     def perform_create(self, serializer):
#         # author_id = self.kwargs.get('pk')
#         # author = Author.objects.get(id=author_id)
#         author = self.request.user.author

#         serializer.save(owner = author)
        


# @api_view(["PUT", "PATCH"])
# @permission_classes([IsAuthenticated])
# def updateInterest (request, pk, id):
#     author = request.user.author
#     interests = author.interest_set.all()
#     id_list = [interest.id for interest in interests]
#     if id in id_list:
#         interest = Interest.objects.get(id = id)
#         serializer = InterstSerializer(interest, data = request.data, many = False)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
    
#     return Response(
#         {"error": "WRONG INTERESTS ID"},
#         status=status.HTTP_400_BAD_REQUEST 
#     )


# @permission_classes([IsAuthenticated])
# class DeleteInterest (generics.DestroyAPIView):
#     queryset = Interest.objects.all()
#     serializer_class = InterstSerializer
#     lookup_field = "id"

#     def perform_destroy(self, instance):
#         author = self.request.user.author

#         if instance.owner.id == author.id:
#             instance.delete()
#         else :
#             return Response(
#         {"error": "WRONG INTERESTS ID"},
#         status=status.HTTP_400_BAD_REQUEST 
#     )




        # recipient_id = self.kwargs.get('pk')

        # return super().perform_create(serializer)








# SCARY CODE, i am just trying how it works
# 
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def interestGetPost (request,pk):
#     method = request.method

#     if method == "GET":
#         userObj = Author.objects.get(id=pk)
#         interestObj = userObj.interest_set.all()
#         interestObj = InterstSerializer(interestObj, many = True)
#         return Response (interestObj.data) 
        
#     if method == "POST":
#         userObj = request.user.author

#         serializer = InterstSerializer(data = request.data)
#         if serializer.is_valid(raise_exception=True):
#             owner = userObj
#             # name = serializer.validated_data.get('name')
#             # description = serializer.validated_data.get('description')
#             try:

#                 name = request.data["name"]
#                 description = request.data["description"]
#             except:
#                 return Response(
#                     {"error": "WRONG INTEREST INFO"},
#                     status=status.HTTP_400_BAD_REQUEST 
#                 )

#             serializer.save(owner=owner)
#             return Response(serializer.data)
        
        







