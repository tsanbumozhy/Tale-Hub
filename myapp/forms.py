from django import forms
from django.core.files import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Stories, Genre, Comment

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    pen_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Pen Name'}))
    profile_photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'my-custom-class'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 35}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        profile_data = {
            'user': user,
            'pen_name': self.cleaned_data['pen_name'],
            'bio': self.cleaned_data['bio'],
        }
        
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            profile_photo_file = File(profile_photo)
            profile_data['profile_photo'] = profile_photo_file
        profile = Profile.objects.create(**profile_data)
        return user, profile



    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pen_name', 'bio', 'profile_photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 35}),
            'pen_name': forms.TextInput(),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'profile_photo'})
        }

class StoryForm(forms.ModelForm):
    genre_id = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple, label='Genre', to_field_name='name')

    class Meta:
        model = Stories
        fields = ['title', 'genre_id', 'description', 'cover_image', 'content_url']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add your comment'}),
        }