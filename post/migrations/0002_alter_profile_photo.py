# Generated by Django 4.2.3 on 2024-09-23 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile/'),
        ),
    ]
