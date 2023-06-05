import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import UserViewSet, ProfileViewSet, GenreViewSet, StoriesViewSet, LikeViewSet, CommentViewSet
from myapp.views import home, genres, genre_stories, create_user, create_story

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

    path('create_story/', create_story, name='create_story'),

    path('genres/', genres, name='genres'),
    path('genre_stories/<str:genre_name>/', genre_stories, name='genre_stories'),
    
    path('create_user/', create_user, name='create_user'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

