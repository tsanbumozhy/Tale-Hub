from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Profile, Genre, Stories, Like, Comment
from .serializers.serializers import UserSerializer, ProfileSerializer, GenreSerializer, StoriesSerializer, LikeSerializer, CommentSerializer
from .forms import RegistrationForm

from django.shortcuts import render, redirect

def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user, profile = form.save()

            return redirect('index.html')
    else:
        form = RegistrationForm()

    return render(request, 'profile/create_user.html', {'form': form})

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
