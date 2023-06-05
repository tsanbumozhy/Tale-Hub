from rest_framework import viewsets
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile, Genre, Stories, Like, Comment
from .serializers.serializers import UserSerializer, ProfileSerializer, GenreSerializer, StoriesSerializer, LikeSerializer, CommentSerializer
from .forms import RegistrationForm, StoryForm

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home(request):
    if request.user.is_authenticated:
        # User is logged in
        username = request.user.username
        user_details = User.objects.get(username=username)
        profile_details = Profile.objects.get(user=user_details.id)
        stories = Stories.objects.all()
        genres = Genre.objects.all()
        return render(request, 'home.html', {'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Stories': stories})
    else:
        # User is not logged in
        return render(request, 'home.html')
    
def genres(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all
    return render(request, 'genres.html', {'User': user_details, 'Profile': profile_details, 'Genres': genres})

def genre_stories(request, genre_name):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    genre = get_object_or_404(Genre, name=genre_name)
    stories = Stories.objects.filter(genre_id=genre.genre_id).order_by('title')
    return render(request, 'genre_stories.html', { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Genre': genre, 'Stories': stories })

def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user, profile = form.save()
            return render(request, 'home.html', {'User': user, 'Profile': profile})
    else:
        form = RegistrationForm()

    return render(request, 'profile/create_user.html', {'form': form})

def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('home')
    else:
        form = StoryForm()

    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    return render(request, 'write.html', {'form': form, 'User': user_details, 'Profile': profile_details, 'Genres': genres})

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        username = self.request.user.username
        print(username)
        return reverse_lazy('home') + '?username=' + username

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class StoriesViewSet(viewsets.ModelViewSet):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('content_url')
        if uploaded_file:
            serializer.save(content_url=uploaded_file)
        else:
            serializer.save()
        
        uploaded_file = self.request.FILES.get('cover_image')
        if uploaded_file:
            serializer.save(cover_image=uploaded_file)
        else:
            serializer.save()

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
