from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api-docs'

router = DefaultRouter()
router.register('blogs', views.BlogSer)
router.register('users', views.AuthorList)
# router.register('interests', views.interest_view)
# router.register('interests', views.InterestList,basename='interests')

urlpatterns = [

    path('auth/', obtain_auth_token),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('', views.getRoutes, name='api'),

    path('blogs/<str:pk>/comment/', views.blogComment),

    path('', include(router.urls)),

    # BLOG
    path('blogs/create/', views.BlogCreate.as_view(), name="list-create" ),
    path('blogs/search', views.BlogListView.as_view()),


    # # TAG
    path('tags/', views.TagList.as_view()),
    # path('blogs/tags/create/', views.CreateTag.as_view()),


    # # AUTHOR
    path('users/register/', views.UserCreate.as_view(), name = 'register'),
    path('users/search/', views.AuthorSearching),

    # # INTEREST
    path('users/<int:pk>/interests/', views.InterestList.as_view({"get" : "list","post" : "create"}), name='interest-list'),
    
    #       +-. 
    path('users/<int:pk>/interests/<int:interest_id>/', views.InterestList.as_view({"get" : "retrieve", "delete" : "destroy", "put" : "update"})),

    # MESSAGE
    path('input-messages/', views.MessageInputList.as_view()),
    path('output-messages/', views.MessageOutputList.as_view()),
    path('create-message/<int:pk>', views.CreateMessage.as_view() ),
    path('docs/', include_docs_urls (title='BlogAPI')),
    path('schema/', get_schema_view(
        title="BlogAPI",
        description="API for my Blog",
        version="1.0.0"
    ), name='schema'),

    path('schema-js/', get_schema_view(
        title="BlogAPI",
        description="API for my Blog",
        version="1.0.0"
    ), name='schema-js'),

]

# urlpatterns += router.urls