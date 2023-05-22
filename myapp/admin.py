from django.contrib import admin
from myapp.models import Profile, Genre, Stories, Like, Comment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Genre)
admin.site.register(Stories)
admin.site.register(Like)
admin.site.register(Comment)
