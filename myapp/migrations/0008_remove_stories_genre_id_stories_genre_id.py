# Generated by Django 4.2.1 on 2023-06-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stories',
            name='genre_id',
        ),
        migrations.AddField(
            model_name='stories',
            name='genre_id',
            field=models.ManyToManyField(to='myapp.genre'),
        ),
    ]
