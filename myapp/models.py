from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.AutoField(primary_key=True)
    pen_name = models.CharField(max_length=250)
    profile_photo = models.ImageField(upload_to='profile_photo/')
    bio = models.TextField()

    def __str__(self):
        return str(self.profile_id)

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.name)

class Stories(models.Model):
    story_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    genre_id = models.ManyToManyField(Genre)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='stories/covers/')
    content_url = models.FileField(upload_to='stories/pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.story_id)

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    story = models.ForeignKey(Stories, on_delete=models.CASCADE)
    liked = models.BooleanField()

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    story = models.ForeignKey(Stories, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
