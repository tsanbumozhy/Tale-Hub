import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import UserViewSet, ProfileViewSet, GenreViewSet, StoriesViewSet, LikeViewSet, CommentViewSet
from myapp.views import home, search, logout_view, genres, genre_stories, create_user, create_story, story_details, edit_profile, like
from myapp.views import my_stories, read_list, favourites, add_comment, edit_comment, delete_comment, view_pdf

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('genres', GenreViewSet)
router.register('stories', StoriesViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('', home, name='home'),

    path('search/', search, name='search'),

    path('create_story/', create_story, name='create_story'),
    path('story/<str:story_id>/', story_details, name='story_details'),

    path('story/<int:story_id>/pdf/', view_pdf, name='view_pdf'),

    path('story/<str:story_id>/like', like, name='add_like'),
    path('story/<int:story_id>/add_comment/', add_comment, name='add_comment'),
    
    path('story/<int:story_id>/edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('story/<int:story_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('genres/', genres, name='genres'),
    path('genre_stories/<str:genre_name>/', genre_stories, name='genre_stories'),
    
    path('create_user/', create_user, name='create_user'),

    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/my_list/', my_stories, name='my_list'),
    path('profile/read_list/', read_list, name='read_list'),
    path('profile/favourites/', favourites, name='liked_stories'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

