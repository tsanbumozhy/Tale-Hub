from django.conf import settings
from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile, Genre, Stories, Like, Comment
from .serializers.serializers import UserSerializer, ProfileSerializer, GenreSerializer, StoriesSerializer, LikeSerializer, CommentSerializer
from .forms import RegistrationForm, ProfileForm, StoryForm, CommentForm

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
    
def search(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    stories = Stories.objects.all()
    genres = Genre.objects.all()
    
    query = request.GET.get('q')
    results = Stories.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'search_results.html', {'results': results, 'query': query, 'User': user_details, 'Profile': profile_details, 'Genres': genres})
    
def logout_view(request):
    logout(request)
    return redirect('home')
    
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
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profile = Profile(
                user=user,
                pen_name=form.cleaned_data['pen_name'],
                bio=form.cleaned_data['bio'],
                profile_photo=request.FILES.get('profile_photo')
            )
            profile.save()

            stories = Stories.objects.all()
            genres = Genre.objects.all()
            return render(request, 'home.html', {'User': user, 'Profile': profile, 'Genres': genres, 'Stories': stories})
    else:
        form = RegistrationForm()
    
    return render(request, 'profile/create_user.html', {'form': form})

def story_details(request, story_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    story = get_object_or_404(Stories, story_id=story_id)

    read = Like.objects.filter(profile=profile_details, story=story)
    if not read:
        Like.objects.create(profile=profile_details, story=story, liked=False)

    like_status = Like.objects.get(profile=profile_details, story=story)

    comments = Comment.objects.filter(story=story)

    read_count = Like.objects.filter(story=story).count()
    likes_count = Like.objects.filter(story=story, liked=True).count()
    comment_count = Comment.objects.filter(story=story).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Story': story, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'story_details.html', context)

def view_pdf(request, story_id):
    try:
        story = Stories.objects.get(story_id=story_id)
    except Stories.DoesNotExist:
        return render(request, 'error.html', {'message': 'Story not found'})

    pdf_file_path = story.content_url.path

    response = FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
    return response

def like(request, story_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    story = get_object_or_404(Stories, story_id=story_id)

    like_status = Like.objects.get(profile=profile_details, story=story)

    like_status.liked = not like_status.liked
    like_status.save()

    comments = Comment.objects.filter(story=story)

    read_count = Like.objects.filter(story=story).count()
    likes_count = Like.objects.filter(story=story, liked=True).count()
    comment_count = Comment.objects.filter(story=story).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Story': story, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'story_details.html', context)

def add_comment(request, story_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    story = get_object_or_404(Stories, story_id=story_id)

    if request.method == 'POST':
        comment_text = request.POST['comment']

        comment = Comment(profile=profile_details, story=story, comment=comment_text)
        comment.save()    

    read = Like.objects.filter(profile=profile_details, story=story)
    if not read:
        Like.objects.create(profile=profile_details, story=story, liked=False)

    like_status = Like.objects.get(profile=profile_details, story=story)

    comments = Comment.objects.filter(story=story)

    read_count = Like.objects.filter(story=story).count()
    likes_count = Like.objects.filter(story=story, liked=True).count()
    comment_count = Comment.objects.filter(story=story).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Story': story, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'story_details.html', context)

def edit_comment(request, story_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        updated_comment_text = request.POST['comment']

        if comment.profile.user == request.user:
            comment.comment = updated_comment_text
            comment.last_updated = timezone.now()
            comment.save()

            messages.success(request, 'Comment updated successfully.')
        else:
            messages.error(request, 'You are not authorized to edit this comment.')

        return redirect('story_details', story_id=comment.story.story_id)

    return redirect('story_details', story_id=comment.story.story_id)

def delete_comment(request, story_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        if comment.profile.user == request.user:
            comment.delete()

            messages.success(request, 'Comment deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this comment.')

        return redirect('story_details', story_id=comment.story.story_id)

    return redirect('story_details', story_id=comment.story.story_id)
    
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

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)

    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all
    
    return render(request, 'profile/edit_profile.html', {'form': form, 'User': user_details, 'Profile': profile_details, 'Genres': genres})

def my_stories(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all

    stories = Stories.objects.filter(author=user_details.id).order_by('title')

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Stories':stories, 'Flag':1 }

    return render(request, 'profile/profile_pages.html', context)

def read_list(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all
    stories = Stories.objects.all

    liked_stories = Stories.objects.filter(like__profile=profile_details)

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Stories':liked_stories, 'Flag':2 }

    return render(request, 'profile/profile_pages.html', context)

def favourites(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    genres = Genre.objects.all
    stories = Stories.objects.all

    liked_stories = Stories.objects.filter(like__profile=profile_details, like__liked=True)

    context = { 'User': user_details, 'Profile': profile_details, 'Genres': genres, 'Stories':liked_stories, 'Flag':3 }

    return render(request, 'profile/profile_pages.html', context)

    story = Story.objects.get(id=story_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user
            comment.save()
            return redirect('story_details', story_id=story_id)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form, 'story': story})

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
