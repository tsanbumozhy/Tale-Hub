# Generated by Django 4.2.1 on 2023-06-12 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_stories_genre_id_stories_genre_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='profile_id',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='story_id',
            new_name='story',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='profile_id',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='story_id',
            new_name='story',
        ),
    ]
