# Generated by Django 4.2.3 on 2024-11-06 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_remove_blogpost_post_profile_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='post',
        ),
    ]
