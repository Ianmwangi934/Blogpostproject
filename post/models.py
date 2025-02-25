from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500,blank=True)
    location = models.CharField(max_length=100,blank=True)
    birth_date = models.DateTimeField(null=True,blank=True)
    photo = models.ImageField(default='default.jpg',upload_to='profile/', null=True, blank=True)
    background_photo = models.ImageField(default='default.jpg',upload_to='profile/', null=True,blank=True)

    def __str__(self):
        return self.user.username

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True,null=True)# optional text content
    image = models.ImageField(upload_to='profile/',blank=True,null=True)
    video = models.FileField(upload_to='profile/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"

    def comments(self):
        return Comment.objects.filter(post=self) # Return all comments related to the post



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.CharField(blank=True,null=True,max_length=1000)

    def __str__(self):
        return f"Commented by {self.user.username} on {self.post.title}"



